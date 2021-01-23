import json
import logging
import os

from azure.storage.blob import BlobServiceClient
import sqlalchemy as sa

from sql_connectors import posts_to_sql, profile_to_sql
from util import extract_posts, extract_profile, read_blob

logger = logging.getLogger(__name__)

blob_service_client = BlobServiceClient.from_connection_string(
    os.environ["AZURE_STORAGE_CONNECTION_STRING"]
)
engine = sa.create_engine(os.environ["DATABASE_CONNECTION_STRING"])


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
            posts_to_sql(con, posts)
            logger.info("committing transaction")
    except sa.exc.IntegrityError as err:
        logger.info(f"Duplicate entry:\n{err}")
