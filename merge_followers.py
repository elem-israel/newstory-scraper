from datetime import datetime
import json
import logging
import os
import sys

import click
from dotenv import load_dotenv
from instapy import smart_run, InstaPy

from utils import upload_to_azure_storage

load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    path = "C:/tmp/newstory/profiles"
    users = os.listdir(path)
    all = []
    for u in users:
        relations_path = os.path.join(path, u, "relations.json")
        if os.path.exists(relations_path):
            with open(relations_path) as fp:
                all.extend(json.load(fp).get("data", {}).get("followers", []))
    out = "C:/tmp/newstory/youth.txt"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fp:
        fp.write("\n".join(sorted(all)))


if __name__ == "__main__":
    main()
