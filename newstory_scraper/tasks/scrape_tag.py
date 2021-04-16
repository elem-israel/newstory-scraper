import json
import logging
import os
from datetime import datetime
from functools import lru_cache

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed

from ..config import get_config
from ..kafka_config import get_producer
from ..scraper import get_tag
from ..util import get_username_by_id

logger = logging.getLogger(__name__)
config = get_config()
destination = config["scraper"]["destination"]


def scrape_tag(tag, maximum=100) -> dict:
    """
    Scrape posts by tag. This returns only basic information about the post owner
    without bio and stuff.
    :param tag: The tag to scrape
    :return:
    """
    posts = get_tag(
        tag, destination=os.path.join(profile_storage_path, "scraper"), maximum=maximum
    )
    path = os.path.join(destination, "tag", tag, f"{tag}.json")
    for i in range(len(posts["GraphImages"])):
        posts["GraphImages"][i]["owner"]["username"] = retry(
            lru_cache(get_username_by_id),
            stop=stop_after_attempt(5),
            wait=wait_fixed(5),
        )(posts["GraphImages"][i]["owner"]["id"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(
        {"created_at": datetime.utcnow().isoformat(), "tag": tag, "data": posts},
        open(path, "w"),
    )
    if config.getboolean("kafka", "enabled"):
        get_producer(config["kafka"]["bootstrap_servers"]).send(
            topic="newstory.tasks.upload", key=tag, value=path
        ).get(timeout=60)
    return posts
