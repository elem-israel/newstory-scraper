from datetime import datetime
import json
import logging
import os

from azure.storage.blob import BlobServiceClient

from kafka_config import get_producer
from scraper import get_profile

logger = logging.getLogger(__name__)

blob_service_client = BlobServiceClient.from_connection_string(
    os.environ["AZURE_STORAGE_CONNECTION_STRING"]
)

profile_storage_path = os.getenv("PROFILE_STORAGE_PATH", "/tmp")


def scrape_profile(user) -> dict:
    profile = get_profile(user, "/tmp/scraper")
    path = os.path.join(profile_storage_path, "profile", user, "profile.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fp:
        json.dump({"created_at": datetime.utcnow().isoformat(), "data": profile}, fp)
    get_producer().send("newstory.tasks.upload", user, path).get(timeout=60)
    return profile
