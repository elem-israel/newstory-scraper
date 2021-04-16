import json
import logging
import os
from datetime import datetime

from instagram_scraper import InstagramScraper

from newstory_scraper.config import get_config
from newstory_scraper.scraper import get_tag
from newstory_scraper.util import get_proxy


logger = logging.getLogger(__name__)
config = get_config()
destination = config["scraper"]["destination"]


def scrape_tag(tag: str, output: str = "./", maximum: int = 100) -> dict:
    """
    Scrape posts by tag. This returns only basic information about the post owner
    without bio and stuff.
    :param maximum: number of posts to get
    :param output: output directory
    :param tag: The tag to scrape
    :return:
    """
    posts = get_tag(
        tag, destination=os.path.join(destination, "scraper"), maximum=maximum
    )
    path = os.path.join(output, "tags", f"{tag}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(
        {
            "created_at": datetime.utcnow().isoformat(),
            "tag": tag,
            "data": posts,
            "type": "tag",
        },
        open(path, "w"),
    )
    return posts


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


class CustomTagScraper(InstagramScraper):
    """Override argument node to disable recursive mechanisms."""

    def augment_node(self, node):
        self.extract_tags(node)

        if "urls" not in node:
            node["urls"] = []
        if node["is_video"] and "video_url" in node:
            node["urls"] = [node["video_url"]]
        elif "__typename" in node and node["__typename"] == "GraphImage":
            node["urls"] = [self.get_original_image(node["display_url"])]

        return node


def get_tag(tag: str, destination: str = ".", maximum=100):
    """
    Scrape posts based on tag search
    :param tag:
    :param destination:
    :param maximum:
    :return:
    """
    proxies = get_proxy()
    logger.info("running instagram scraper")
    kwargs = {
        "usernames": [tag],
        "destination": destination,
        "media_metadata": True,
        "profile_metadata": False,
        "media_types": ["none"],
        "maximum": maximum + 50,
        "tag": tag is not None,
        "comments": False,  # TODO comments are not working https://github.com/arc298/instagram-scraper/issues/615
        "no_check_certificate": True if len(proxies) else False,
        "proxies": json.dumps(proxies) if len(proxies) else None,
    }
    scraper = CustomTagScraper(**kwargs)
    scraper.scrape_hashtag()
    try:
        with open(os.path.join(destination, f"{ tag}.json"), encoding="utf8") as fp:
            return json.load(fp)
    except FileNotFoundError:
        raise ValueError("Failed to scrape tag. View logs for more info.")
