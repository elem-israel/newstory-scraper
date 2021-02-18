import json
import logging
import os
from datetime import datetime

from kafka_config import get_producer
from . import bootstrap_servers, blob_service_client

logger = logging.getLogger(__name__)


def upload(path) -> str:
    container_name = os.environ["CONTAINER_NAME"]
    with open(path, "r") as fp:
        profile = json.load(fp)
    date = datetime.fromisoformat(profile["created_at"]).isoformat().split("T")[0]
    user = profile["data"]["GraphProfileInfo"]["username"]
    blob = "/".join(["profiles", date, user, "profile.json"])
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob
    )
    with open(path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    get_producer(bootstrap_servers).send("newstory.tasks.newentry", user, blob).get(
        timeout=60
    )
    return blob
