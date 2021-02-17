from datetime import datetime
import json
import logging
import os
import sys
import tempfile
from time import sleep

import click
from dotenv import load_dotenv

from scraper import get_profile

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)
load_dotenv()


@click.command()
@click.argument("users", required=False)
@click.option("--file", "input_file", type=click.File("r"))
@click.option("--out", "out_dir", type=click.Path(), default="output")
def main(users, input_file, out_dir):
    if users:
        users_list = users.split(",")
    elif input_file:
        users_list = input_file.read().split("\n")
    else:
        raise Exception("inout_file or users must be provided")
    first = True
    for u in users_list:
        if not first:
            sleep(30)
        first = False
        print(f"processing {u}")
        destination = os.getenv("INSTAGRAM_SCRAPER_DESTINATION")
        if destination is None:
            temp_dir = tempfile.TemporaryDirectory()
            destination = temp_dir.name
        try:
            profile = get_profile(u, destination)
        except ValueError:
            logger.warning(f"User note found: {u}")
            continue
        if out_dir is not None:
            user_dir = os.path.join(out_dir, u)
            user_path = os.path.join(user_dir, "profile.json")
            os.makedirs(user_dir, exist_ok=True)
            with open(user_path, "w") as fp:
                json.dump(
                    {"created_at": datetime.utcnow().isoformat(), "data": profile}, fp
                )
        else:
            print(json.dumps(profile, 2))


if __name__ == "__main__":
    main()
