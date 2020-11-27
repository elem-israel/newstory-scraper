from datetime import datetime
import json
import os
import logging
import sys

from azure.storage.blob import BlobServiceClient

from . import consumers
from .scraper import get_profile

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


if int(os.getenv("WORKER", 0)):
    blob_service_client = BlobServiceClient.from_connection_string(
        os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    )


def test(event):
    event_data = event.value
    # Do whatever you want
    print(event_data)


def scrape_profile(user) -> dict:
    profile = get_profile(user, "/tmp/scraper")
    path = f"/tmp/profiles/{user}/profile.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fp:
        json.dump({"created_at": datetime.utcnow().isoformat(), "data": profile}, fp)
    upload.apply_async(args=[path])
    return profile


def upload(path) -> str:
    container_name = os.environ["CONTAINER_NAME"]
    with open(path, "r") as fp:
        profile = json.load(fp)
    date = datetime.fromisoformat(profile["created_at"]).isoformat().split("T")[0]
    user = profile["data"]["GraphProfileInfo"]["username"]
    blob = f"profiles/{date}/{user}/profile.json"
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob
    )
    with open(path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    return blob


tasks = {"profile": scrape_profile, "test": test}


def main(topic):
    logger.info(f"listening to: {topic}")
    for event in consumers.get(topic):
        tasks[event.topic](event)
