import logging
import os
import sys

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass
from kafka_config import get_producer

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

bootstrap_servers = [
    f'{os.getenv("KAFKA_HOST", "localhost")}:{os.getenv("KAFKA_PORT", "9092")}'
]

if __name__ == "__main__":
    f = get_producer(bootstrap_servers).send(
        topic=sys.argv[1], key=sys.argv[2], value=sys.argv[3]
    )
    print(f.get(timeout=10))
