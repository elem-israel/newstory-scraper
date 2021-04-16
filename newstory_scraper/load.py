import json
import logging
from datetime import datetime

import sqlalchemy as sa
from azure.storage.blob import BlobServiceClient

from newstory_scraper.config import get_config
from newstory_scraper.sql_connectors import photos_to_sql
from newstory_scraper.sql_connectors import posts_to_sql
from newstory_scraper.sql_connectors import tags_to_sql
from newstory_scraper.util import traverse_path

logger = logging.getLogger(__name__)

config = get_config()
blob_service_client = BlobServiceClient.from_connection_string(
    config["azure"]["storage_connection_string"]
)


def upload_photos(posts):
    res = []
    for post in posts:
        date = post["created_date"].strftime("%Y-%m-%d")
        post_id = post["instagram_post_id"]
        blob = f"images/{date}/{post['instagram_post_id']}.jpg"
        blob_client = blob_service_client.get_blob_client(
            container=config["azure"]["container_name"],
            blob=blob,
        )
        # blob_client.upload_blob_from_url(post["image"], overwrite=True)
        res.append({"photo_path": blob, "post_id": post_id})
    return res


def datetime_parser(dct):
    for k, v in dct.items():
        try:
            dct[k] = datetime.fromisoformat(v)
        except (ValueError, TypeError):
            pass
    return dct


def load(source: str):
    engine = sa.create_engine(config["database"]["connection_string"])
    for item in traverse_path(source):
        with engine.begin() as con:
            data = json.load(open(item), object_hook=datetime_parser)
            if data.get("posts"):
                posts_to_sql(con, data["posts"])
                images = upload_photos(data["posts"])
                photos_to_sql(con, images)
            if data.get("profile"):
                raise NotImplementedError
            if data.get("hashtags"):
                tags_to_sql(con, data["hashtags"])
