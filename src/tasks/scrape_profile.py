import json
import logging
import os
from datetime import datetime

from kafka_config import get_producer
from scraper import get_profile
from . import bootstrap_servers, profile_storage_path

logger = logging.getLogger(__name__)


def scrape_profile(user: str) -> dict:
    profile = get_profile(user, os.path.join(profile_storage_path, "scraper"))
    path = os.path.join(profile_storage_path, "profile", user, "profile.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fp:
        json.dump({"created_at": datetime.utcnow().isoformat(), "data": profile}, fp)
    get_producer(bootstrap_servers).send(
        "newstory.tasks.upload", key=user.encode(), value=path
    ).get(timeout=60)
    return profile
