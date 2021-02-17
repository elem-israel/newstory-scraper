from datetime import datetime
import json
import logging
import os

from azure.storage.blob import BlobServiceClient

from kafka_config import producer
from scraper import get_profile

logger = logging.getLogger(__name__)

blob_service_client = BlobServiceClient.from_connection_string(
    os.environ["AZURE_STORAGE_CONNECTION_STRING"]
)


def scrape_profile(user) -> dict:
    profile = get_profile(user, "/tmp/scraper")
    path = f"/tmp/profiles/{user}/profile.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fp:
        json.dump({"created_at": datetime.utcnow().isoformat(), "data": profile}, fp)
    producer.send("newstory.tasks.upload", user, path).get(timeout=60)
    return profile
