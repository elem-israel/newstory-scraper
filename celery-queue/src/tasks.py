from datetime import datetime
import json
import os
import time

from celery import Celery
from requests import HTTPError

from scraper import get_profile

CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name="tasks.echo")
def hello(string: str) -> str:
    time.sleep(5)
    print(string)
    return string


@celery.task(
    name="tasks.profile",
    autoretry_for=(HTTPError, ValueError),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def scrape_profile(user) -> None:
    profile = get_profile(user, "/tmp/scraper")
    profile_path = f"/tmp/profiles/{user}/profile.json"
    os.makedirs(os.path.dirname(profile_path), exist_ok=True)
    with open(profile_path, "w") as fp:
        json.dump({"created_at": datetime.utcnow().isoformat(), "data": profile}, fp)
    return profile
