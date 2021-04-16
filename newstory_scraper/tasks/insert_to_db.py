import json
import logging
import os

import sqlalchemy as sa

from . import blob_service_client, engine
from ..sql_connectors import posts_to_sql, profile_to_sql, photos_to_sql
from ..util import extract_posts, extract_profile, read_blob

logger = logging.getLogger(__name__)


def insert_to_db(blob, container_name=None):
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
            photos = [
                {
                    "username": user,
                    "photo_path": f"/profiles/{date}/{user}/{post['instagram_post_id']}_{i+1}.jpg",
                    "post_id": post["instagram_post_id"],
                }
                for i in range(len(post["photos"]))
                for post in posts
            ]
            photos_to_sql(con, photos)
            posts_to_sql(con, posts)
            logger.info("committing transaction")
    except sa.exc.IntegrityError as err:
        logger.info(f"Duplicate entry:\n{err}")
