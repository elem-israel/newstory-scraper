import logging
import sys

sys.path += ["celery-queue/src"]

import click
from dotenv import load_dotenv
from scraper import scrape_profile

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

load_dotenv()


@click.group()
@click.option("--users", "users", type=click.File("r"))
@click.option("--out", "out_dir", type=click.Path(), default="output")
@click.pass_context
def main(ctx, users, out_dir):
    ctx.ensure_object(dict)
    ctx.obj["users"] = users
    ctx.obj["out_dir"] = out_dir


@main.command()
@click.pass_context
@click.argument("user", required=False)
def profile(ctx, user):
    if ctx.obj["users"]:
        print("reading from file")
        users = ctx.obj["users"].read().split("\n")
    else:
        if user is None:
            print("error: Missing user", file=sys.stderr)
            exit(1)
        users = [user]
    for u in users:
        print(f"processing {u}")
        scrape_profile(u, out_dir=ctx.obj["out_dir"])


if __name__ == "__main__":
    main()
