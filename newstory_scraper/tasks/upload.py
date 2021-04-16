import json
import logging
import os
from datetime import datetime

from . import blob_service_client
from ..config import get_config
from ..kafka_config import get_producer
from ..util import extract_posts

logger = logging.getLogger(__name__)

config = get_config()


def upload_profile(path) -> str:
    container_name = config["azure"]["container"]
    with open(path, "r") as fp:
        profile = json.load(fp)
    date = datetime.fromisoformat(profile["created_at"]).isoformat().split("T")[0]
    user = profile["data"]["GraphProfileInfo"]["username"]
    posts = extract_posts(profile)
    for post in posts:
        for i, photo in enumerate(post["photos"]):
            blob_client = blob_service_client.get_blob_client(
                container=container_name,
                blob=f"profiles/{date}/{user}/{post['instagram_post_id']}_{i+1}.jpg",
            )
            blob_client.upload_blob_from_url(photo, overwrite=True)
    blob = f"profiles/{date}/{user}/profile.json"
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob
    )
    with open(path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    if config.getboolean("kafka", "enabled"):
        get_producer(config["kafka"]["bootstrap_servers"]).send(
            topic="newstory.tasks.newentry", key=user, value=blob
        ).get(timeout=60)
    return blob


def upload_tag(path) -> str:
    container_name = config["azure"]["container"]
    with open(path, "r") as fp:
        data = json.load(fp)
    date = datetime.fromisoformat(data["created_at"]).isoformat().split("T")[0]
    tag = data["tag"]
    posts = extract_posts(data)
    for post in posts:
        for i, photo in enumerate(post["photos"]):
            blob_client = blob_service_client.get_blob_client(
                container=container_name,
                blob=f"tag/{date}/{tag}/{post['instagram_post_id']}_{i + 1}.jpg",
            )
            blob_client.upload_blob_from_url(photo, overwrite=True)
    blob = f"profiles/{date}/{tag}/tag.json"
    if config.getboolean("kafka", "enabled"):
        get_producer(config["kafka"]["bootstrap_servers"]).send(
            topic="newstory.tasks.newentry", key=tag, value=blob
        ).get(timeout=60)
    return blob
