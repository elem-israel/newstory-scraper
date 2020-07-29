import sys

from instapy import set_workspace

sys.path += ["celery-queue/src"]

import os
import click
from dotenv import load_dotenv
from scraper import scrape


load_dotenv()


@click.command()
@click.argument("user", required=False)
@click.option("--file", "input_file", type=click.File("r"))
@click.option("--out", "out_dir", type=click.Path(), default="output")
@click.option("--workspace", "workspace", type=click.Path())
def main(user, input_file, out_dir, workspace):
    if workspace:
        set_workspace(path=workspace)
    if input_file:
        print("reading from file")
        users = input_file.read().split("\n")
    else:
        users = [user]
    for u in users:
        print(f"processing {u}")
        scrape(u, os.environ["INSTA_USER"], os.environ["INSTA_PASSWORD"], out_dir=out_dir)


if __name__ == "__main__":
    main()
