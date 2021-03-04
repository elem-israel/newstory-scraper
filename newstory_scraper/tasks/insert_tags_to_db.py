import json
import logging
import os

import sqlalchemy as sa

from sql_connectors import tags_to_sql
from . import blob_service_client, engine
from util import read_blob, extract_tags

logger = logging.getLogger(__name__)


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
