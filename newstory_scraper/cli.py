import logging
import sys

import click
from dotenv import load_dotenv

from newstory_scraper.extract import scrape_tag
from newstory_scraper.load import load
from newstory_scraper.tasks.scrape_profile import scrape_profile
from newstory_scraper.transform import transform

load_dotenv()


@click.group()
def cli():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    pass


@cli.group()
def extract():
    pass


@extract.command("user")
@click.argument("user")
def cli_extract_user(user):
    """
    Scrape posts by tag from instagram
    """
    click.echo(scrape_profile(user))


@extract.command("tag")
@click.option(
    "-o",
    "--output",
    type=click.types.Path(dir_okay=True, file_okay=False, exists=False, writable=True),
)
@click.argument("tag")
@click.argument("n", default=1)
def cli_extact_tag(output, tag, n):
    """
    Scrape posts by tag from instagram
    """
    click.echo(scrape_tag(tag, output=output, maximum=n))


@cli.command("transform")
@click.argument(
    "source",
    type=click.types.Path(dir_okay=True, file_okay=False, exists=True, readable=True),
)
@click.argument(
    "target",
    type=click.types.Path(dir_okay=True, file_okay=False, exists=False, writable=True),
)
def cli_transform(source, target):
    transform(source, target)


@cli.command("load")
@click.argument(
    "source",
    type=click.types.Path(dir_okay=True, file_okay=False, exists=True, readable=True),
)
def cli_load(source):
    load(source)


if __name__ == "__main__":
    cli()
