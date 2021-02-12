from datetime import datetime
import json
import logging
import os

from azure.storage.blob import BlobServiceClient

from kafka_config import producer

logger = logging.getLogger(__name__)

blob_service_client = BlobServiceClient.from_connection_string(
    os.environ["AZURE_STORAGE_CONNECTION_STRING"]
)


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
    producer.send("newstory.tasks.newEntry", user, blob).get(timeout=60)
    return blob
