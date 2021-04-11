from datetime import datetime
import json
import os
import logging

from azure.storage.blob import BlobServiceClient, upload_blob_to_url
import sqlalchemy as sa

from . import producer
from .scraper import get_profile
from .sql_connectors import posts_to_sql, profile_to_sql, photos_to_sql
from .util import extract_posts, extract_profile, read_blob

logger = logging.getLogger(__name__)

blob_service_client = BlobServiceClient.from_connection_string(
    os.environ["AZURE_STORAGE_CONNECTION_STRING"]
)
engine = sa.create_engine(os.environ["DATABASE_CONNECTION_STRING"])


def echo(text):
    logger.info(text)


def scrape_profile(user) -> dict:
    profile = get_profile(user, "/tmp/scraper")
    path = f"/tmp/profiles/{user}/profile.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fp:
        json.dump({"created_at": datetime.utcnow().isoformat(), "data": profile}, fp)
    producer.send("newstory.tasks.upload", user, path).get(timeout=60)
    return profile


def insert_to_db(blob, container_name=None) -> dict:
    logger.info(f"getting {blob}")
    data = read_blob(
        blob_service_client, container_name or os.environ["CONTAINER_NAME"], blob
    )
    parsed = json.loads(data)
    logger.info("starting transaction")
    try:
        with engine.begin() as con:
            logger.info("inserting profile")
            profile = extract_profile(parsed)
            profile_to_sql(con, profile)
            logger.info("inserting posts")
            posts = extract_posts(parsed)
            logger.info("inserting photos")
            date = profile["created_date"].isoformat().split("T")[0]
            user = profile["username"]
            photos=[]
            for post in posts:
                photos += [{"username": user, "photo_path": f"/profiles/{date}/{user}/{post['instagram_post_id']}_{i+1}.jpg",
                           "post_id": post["instagram_post_id"]} for i in range(len(post["photos"]))]
            photos_to_sql(con, photos)
            print("Done ", path)
            logger.info("committing transaction")
    except sa.exc.IntegrityError as err:
        logger.info(f"Duplicate entry:\n{err}")


def upload(path) -> str:
    container_name = os.environ["CONTAINER_NAME"]
    with open(path, "r") as fp:
        profile = json.load(fp)
    date = datetime.fromisoformat(
        profile["created_at"]).isoformat().split("T")[0]
    user = profile["data"]["GraphProfileInfo"]["username"]
    posts = extract_posts(profile)
    for post in posts:
        for i, photo in enumerate(post["photos"]):
                blob_client = blob_service_client.get_blob_client(
                    container=container_name, blob=f"profiles/{date}/{user}/{post['instagram_post_id']}_{i+1}.jpg"
                )
                blob_client.upload_blob_from_url(photo, overwrite=True)
    blob = f"profiles/{date}/{user}/profile.json"
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob
    )
    with open(path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    producer.send("newstory.tasks.newEntry", user, blob).get(timeout=60)
    return blob
