from datetime import datetime
import json
import logging
import os

from instagram_scraper import InstagramScraper

log = logging.getLogger(__name__)


def dump_json(obj, dest):
    with open(dest, "w+", encoding="utf8") as fp:
        json.dump(
            {"data": obj, "created_at": datetime.now().isoformat()},
            fp,
            indent=2,
            ensure_ascii=False,
        )


def get_profile(user: str):
    log.info("running instagram scraper")
    scraper = InstagramScraper(
        usernames=[user],
        destination="temp",
        media_metadata=True,
        profile_metadata=True,
        media_types=["none"],
        # include_location=True,
        comments=True,
        maximum=100,
    )
    scraper.scrape()
    with open(f"temp/{user}.json", encoding="utf8") as scraped:
        res = json.load(scraped)
    return res


def get_relations(user: str, login_user: str, login_password: str, path: str):
    log.info("running instapy")
    session = InstaPy(
        username=login_user, password=login_password, headless_browser=True
    )
    with smart_run(session):
        followers = session.grab_followers(
            username=user, amount="full", live_match=True, store_locally=True
        )
        following = session.grab_following(
            username=user, amount="full", live_match=True, store_locally=True
        )
    res = {"followers": followers, "following": following}
    dump_json(res, path)
    return


def scrape_profile(user: str, out_dir):
    out_path = os.path.join(out_dir, user)
    os.makedirs(out_path, exist_ok=True)
    profile_path = os.path.join(out_path, "profile.json")
    res = get_profile(user)
    with open(profile_path, "w") as fp:
        json.dump(res, fp)
