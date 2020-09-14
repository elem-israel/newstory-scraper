import os
import time
from celery import Celery
from scraper import scrape_profile as scraper


CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name="tasks.add")
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y


@celery.task(name="tasks.scrape")
def scrape(user) -> None:
    return scraper(user, os.getenv("USER"), os.getenv("PASSWORD"))
