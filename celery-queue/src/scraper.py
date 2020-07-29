from datetime import datetime
import json
import logging
import os
import sys
from instagram_scraper import InstagramScraper
from instapy import InstaPy, smart_run

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger().setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
log = logging.getLogger(__name__)


def dump_json(obj, dest):
    with open(dest, "w+", encoding="utf8") as fp:
        json.dump(
            {"data": obj, "created_at": datetime.now().isoformat()},
            fp,
            indent=2,
            ensure_ascii=False,
        )


def get_profile(user: str, login_user: str, login_password: str, path: str):
    log.info("running instagram scraper")
    scraper = InstagramScraper(
        usernames=[user],
        destination="temp",
        media_metadata=True,
        profile_metadata=True,
        media_types=["none"],
    )
    scraper.scrape()
    with open(f"temp/{user}.json", encoding="utf8") as scraped:
        res = json.load(scraped)
        dump_json(res, path)
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


def scrape(user: str, login_user: str, login_password: str, out_dir: str = "output"):
    out_path = os.path.join(out_dir, user)
    os.makedirs(out_path, exist_ok=True)
    profile_path = os.path.join(out_path, "profile.json")
    relations_path = os.path.join(out_path, "relations.json")
    if not os.path.exists(profile_path):
        get_profile(user, login_user, login_password, profile_path)
    if not os.path.exists(relations_path):
        get_relations(user, login_user, login_password, relations_path)
