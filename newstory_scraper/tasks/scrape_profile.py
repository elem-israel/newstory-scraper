import json
import logging
import os
from datetime import datetime

from . import bootstrap_servers
from ..config import get_config
from ..kafka_config import get_producer
from ..scraper import get_profile

logger = logging.getLogger(__name__)
config = get_config()
destination = config["scraper"]["destination"]


def scrape_profile(user) -> dict:
    """
    Retrieve a user profile and dump it locally as a json.
    :param user: The user to scrape
    :return:
    """
    profile = get_profile(user, destination, "scraper")
    path = os.path.join(destination, "profile", user, "profile.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(
        {"created_at": datetime.utcnow().isoformat(), "data": profile}, open(path, "w")
    )
    if config.getboolean("kafka", "enabled"):
        get_producer(bootstrap_servers).send(
            topic="newstory.tasks.upload", key=user, value=path
        ).get(timeout=60)
    return profile
