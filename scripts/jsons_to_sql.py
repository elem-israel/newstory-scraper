import logging
import sys

from dotenv import load_dotenv

load_dotenv()

from worker.src.tasks import insert_to_db

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if __name__ == "__main__":
    insert_to_db("profiles/2020-11-24/_eden.nnn_/profile.json")
