import json
import logging
import os
import sys

import click
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def comma_separated(ctx, param, value):
    if value is not None:
        return value.split(",")


@click.command()
@click.option(
    "input-dir", type=click.Path(dir_okay=True, file_okay=False), required=False
)
@click.argument("out", type=click.File("w"))
def main(input_dir, out, profiles):
    profiles = os.listdir(input_dir)
    all = []
    for u in profiles:
        relations_path = os.path.join(input_dir, u, "relations.json")
        if os.path.exists(relations_path):
            with open(relations_path) as fp:
                all.extend(json.load(fp).get("data", {}).get("followers", []))
    os.makedirs(os.path.dirname(out.name), exist_ok=True)
    out.write("\n".join(sorted(all)))


if __name__ == "__main__":
    main()
