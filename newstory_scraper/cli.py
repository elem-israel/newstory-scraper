import logging
import sys

import click
from dotenv import load_dotenv

from newstory_scraper.tasks.scrape_tag import scrape_tag

load_dotenv()


@click.group()
def cli():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    pass


@cli.group()
def scrape():
    pass


@scrape.command("tag")
@click.argument("tag")
def cli_scrape_tag(tag):
    """
    Scrape posts by tag from instagram
    """
    click.echo(scrape_tag(tag, maximum=1))


if __name__ == "__main__":
    cli()
