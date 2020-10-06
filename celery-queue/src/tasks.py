from datetime import datetime
import json
import os
import time

from . import app
from requests import HTTPError
from azure.storage.blob import BlobServiceClient

from .scraper import get_profile

if int(os.getenv("WORKER", 0)):
    blob_service_client = BlobServiceClient.from_connection_string(
        os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    )


@app.task(name="tasks.echo")
def hello(string: str) -> str:
    time.sleep(5)
    print(string)
    return string


@app.task(
    name="tasks.profile",
    autoretry_for=(HTTPError, ValueError),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    rate_limit="2/h",
)
def scrape_profile(user) -> dict:
    profile = get_profile(user, "/tmp/scraper")
    profile_path = f"/tmp/profiles/{user}/profile.json"
    os.makedirs(os.path.dirname(profile_path), exist_ok=True)
    with open(profile_path, "w") as fp:
        json.dump({"created_at": datetime.utcnow().isoformat(), "data": profile}, fp)
    upload.apply_async(args=[user, profile_path])
    return profile


@app.task(name="tasks.upload")
def upload(user, path) -> str:
    container_name = os.environ["CONTAINER_NAME"]
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=f"profiles/{user}/profile.json"
    )
    with open(path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    return "done"
