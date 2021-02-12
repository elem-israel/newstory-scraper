import logging
import sys
from uuid import uuid4

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass
from src import producers

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    f = producers[sys.argv[1]].send(sys.argv[1], sys.argv[2])
    f.get(timeout=0)
