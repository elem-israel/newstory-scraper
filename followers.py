from datetime import datetime
import json
import logging
import os
import sys

import click
from dotenv import load_dotenv
from instapy import smart_run, InstaPy

from scraper import get_relations
from utils import upload_to_azure_storage

load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


@click.command()
@click.argument("users", required=False)
@click.option("--file", "input_file", type=click.File("r"))
@click.option("--out", "out_dir", type=click.Path(), default="output")
@click.option("--max-followers", type=int)
@click.option("--cloud", type=bool)
def main(users, input_file, out_dir, max_followers, cloud):
    if users:
        users_list = users.split(",")
    elif input_file:
        users_list = [u for u in input_file.read().split("\n") if not u.startswith("#")]
    else:
        raise Exception("file or users must be provided")
    session = InstaPy(
        username=os.environ["INSTAPY_USER"],
        password=os.environ["INSTAPY_PASSWORD"],
        headless_browser=True,
        browser_executable_path="C:/Program Files/Mozilla Firefox/firefox.exe",
    )
    with smart_run(session):
        for u in users_list:
            if u.startswith("#"):
                continue
            logger.info(f"processing {u}")
            user_dir = os.path.join(out_dir, u)
            user_path = os.path.join(user_dir, "relations.json")
            relations = get_relations(session, u, max_followers=max_followers or "full")
            os.makedirs(user_dir, exist_ok=True)
            created_at = datetime.utcnow()
            with open(user_path, "w") as fp:
                json.dump({"created_at": created_at.isoformat(), "data": relations}, fp)
            if cloud:
                cloud_path = os.path.join(
                    "profiles",
                    created_at.strftime("%Y-%m-%d"),
                    user_dir,
                    "relations.json",
                )
                upload_to_azure_storage(
                    os.environ["AZURE_STORAGE_CONNECTION_STRING"],
                    user_path,
                    os.environ["AZURE_STORAGE_CONTAINER"],
                    cloud_path,
                )


if __name__ == "__main__":
    main()
