import json
import logging
import os
import sys

from instagram_scraper import InstagramScraper

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_profile(user: str, destination: str):
    logger.info("running instagram scraper")
    scraper = InstagramScraper(
        usernames=[user],
        destination=destination,
        media_metadata=True,
        profile_metadata=True,
        media_types=["none"],
        maximum=3,
        comments=True,
    )
    scraper.scrape()
    try:
        with open(os.path.join(destination, f"{user}.json"), encoding="utf8") as fp:
            return json.load(fp)
    except FileNotFoundError:
        raise ValueError("User not found. Maybe private profile?")


def get_relations(
    session, user: str, max_followers: int = "full", followers=True, following=False,
):
    logger.info("running instapy")
    res = {}
    if followers:
        res["followers"] = session.grab_followers(
            username=user, amount=max_followers, live_match=True, store_locally=False,
        )
    if following:
        res["following"] = session.grab_following(
            username=user, amount=100, live_match=True, store_locally=False
        )
    return res
