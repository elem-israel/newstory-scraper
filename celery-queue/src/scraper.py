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
    with open(dest, "w+") as fp:
        json.dump({"data": obj, "created_at": datetime.now().isoformat()}, fp, indent=2)


def scrape(user: str, login_user: str, login_password: str):
    outdir = "output/{}".format(user)
    os.makedirs(outdir, exist_ok=True)
    # profile_path = os.path.join(outdir, "profile.json")
    followers_path = os.path.join(outdir, "followers.json")
    # if not os.path.exists(profile_path):
    #     log.info("running instagram scraper")
    #     scraper = InstagramScraper(
    #         usernames=[user],
    #         destination="temp",
    #         media_metadata=True,
    #         profile_metadata=True,
    #         media_types=[],
    #         maximum=10,
    #     )
    #     scraper.scrape()
    # with open("temp/{u}.json".format(u=user), encoding="utf8") as scraped:
    #     profile = json.load(scraped)
    #     dump_json(profile, profile_path)
    if not os.path.exists(followers_path):
        log.info("running instapy")
        session = InstaPy(
            username=login_user, password=login_password, headless_browser=True
        )
        with smart_run(session):
            followers = session.grab_followers(
                username=user, amount=100, live_match=True, store_locally=True
            )
        dump_json(followers, followers_path)
    with open(followers_path) as fp:
        followers = json.load(fp)
    return {"followers": followers}


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    scrape("popeye", os.environ["USER"], os.environ["PASSWORD"])
