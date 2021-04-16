import json
import logging
import os

from instagram_scraper import InstagramScraper

from newstory_scraper.util import get_proxy

logger = logging.getLogger(__name__)


def get_profile(user: str, destination: str, maximum=100):
    proxies = get_proxy()
    logger.info("running instagram scraper")
    kwargs = {
        "usernames": [user],
        "destination": destination,
        "media_metadata": True,
        "profile_metadata": True,
        "media_types": ["none"],
        "maximum": maximum,
        "comments": False,  # TODO comments are not working https://github.com/arc298/instagram-scraper/issues/615
        "no_check_certificate": True if len(proxies) else False,
        "proxies": json.dumps(proxies) if len(proxies) else None,
    }
    scraper = InstagramScraper(**kwargs)
    scraper.scrape()
    try:
        return json.load(
            open(os.path.join(destination, f"{user or tag}.json"), encoding="utf8")
        )
    except FileNotFoundError:
        raise ValueError("Failed to scrape profile not found. View logs for more info.")


def get_relations(
    session, user: str, max_followers: int = "full", followers=True, following=False
):
    logger.info("running instapy")
    res = {}
    if followers:
        res["followers"] = session.grab_followers(
            username=user, amount=max_followers, live_match=True, store_locally=False
        )
    if following:
        res["following"] = session.grab_following(
            username=user, amount=100, live_match=True, store_locally=False
        )
    return res
