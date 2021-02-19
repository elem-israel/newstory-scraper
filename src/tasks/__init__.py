import logging
import os

import sqlalchemy as sa
from azure.storage.blob import BlobServiceClient

logger = logging.getLogger(__name__)
try:
    blob_service_client = BlobServiceClient.from_connection_string(
        os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    )
except KeyError:
    blob_service_client = None
    logger.warning("AZURE_STORAGE_CONNECTION_STRING is not defined")
try:
    engine = sa.create_engine(os.environ["DATABASE_CONNECTION_STRING"])
except KeyError:
    engine = None
    logger.warning("DATABASE_CONNECTION_STRING is not defined")
bootstrap_servers = [
    f'{os.getenv("KAFKA_HOST", "localhost")}:{os.getenv("KAFKA_PORT", "9092")}'
]
profile_storage_path = os.getenv("PROFILE_STORAGE_PATH", "/tmp")
