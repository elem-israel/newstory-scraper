import logging
import sys

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass
from kafka_config import get_producer

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    f = get_producer().send(sys.argv[1], sys.argv[2])
    print(f.get(timeout=10))
