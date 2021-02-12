import json
import logging
import os

from azure.storage.blob import BlobServiceClient
import sqlalchemy as sa

from sql_connectors import tags_to_sql
from util import read_blob, extract_tags

logger = logging.getLogger(__name__)

blob_service_client = BlobServiceClient.from_connection_string(
    os.environ["AZURE_STORAGE_CONNECTION_STRING"]
)
engine = sa.create_engine(os.environ["DATABASE_CONNECTION_STRING"])


def insert_tags_to_db(blob, container_name=None) -> dict:
    logger.info(f"getting {blob}")
    data = read_blob(
        blob_service_client, container_name or os.environ["CONTAINER_NAME"], blob
    )
    parsed = json.loads(data)
    logger.info("starting transaction")
    try:
        with engine.begin() as con:
            logger.info("inserting hashtags")
            tags = extract_tags(parsed)
            tags_to_sql(con, tags)
    except sa.exc.IntegrityError as err:
        logger.info(f"Duplicate entry:\n{err}")
