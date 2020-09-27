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


def get_relations(
    session, user: str, max_followers: int = "full", followers=True, following=False,
):
    logger.info("running instapy")
    res = {}
    if followers:
        res["followers"] = session.grab_followers(
            username=user,
            amount=max_followers,
            live_match=False,
            store_locally=True,
        )
    if following:
        res["following"] = session.grab_following(
            username=user, amount=100, live_match=True, store_locally=True
        )
    return res


@click.command()
@click.argument("users", required=False)
@click.option("--file", "input_file", type=click.File("r"))
@click.option("--out", "out_dir", type=click.Path(), default="output")
@click.option("--workspace", type=click.Path())
@click.option("--max-followers", type=int)
@click.option("--cloud", type=bool)
def main(users, input_file, out_dir, max_followers, workspace, cloud):
    if users:
        users_list = users.split(",")
    elif input_file:
        users_list = input_file.read().split("\n")
    else:
        raise Exception("inout_file or users must be provided")
    session = InstaPy(
        username=os.environ["INSTAPY_USER"],
        password=os.environ["INSTAPY_PASSWORD"],
        headless_browser=True,
    )
    with smart_run(session):
        for u in users_list:
            print(f"processing {u}")
            user_dir = os.path.join(out_dir, u)
            user_path = os.path.join(user_dir, "relations.json")
            relations = get_relations(session, u, max_followers=max_followers,)
            os.makedirs(user_dir, exist_ok=True)
            with open(user_path, "w") as fp:
                json.dump(
                    {"created_at": datetime.utcnow().isoformat(), "data": relations}, fp
                )
            if cloud:
                upload_to_azure_storage(
                    os.environ["AZURE_STORAGE_CONNECTION_STRING"],
                    user_path,
                    os.environ["AZURE_STORAGE_CONTAINER"],
                    user_path,
                )


if __name__ == "__main__":
    main()
