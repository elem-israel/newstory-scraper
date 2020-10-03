import json
import logging
import os
import sys

import click
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


@click.command()
@click.argument("input-dir", type=click.Path(dir_okay=True, file_okay=False))
@click.argument("out", type=click.File("w"))
def main(input_dir, out):
    users = os.listdir(input_dir)
    all = []
    for u in users:
        relations_path = os.path.join(input_dir, u, "relations.json")
        if os.path.exists(relations_path):
            with open(relations_path) as fp:
                all.extend(json.load(fp).get("data", {}).get("followers", []))
    os.makedirs(os.path.dirname(out.name), exist_ok=True)
    out.write("\n".join(sorted(all)))


if __name__ == "__main__":
    main()
