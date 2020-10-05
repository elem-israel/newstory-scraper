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

print("worker started")

@celery.task(name="tasks.add")
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y


@celery.task(name="tasks.hello")
def hello() -> str:
    time.sleep(5)
    print("hello world")
    return "hello world"


@celery.task(name="tasks.profile", autoretry_for=(HTTPError,), retry_backoff=True)
def profile(user) -> None:
    return get_profile(user, "/tmp/artifacts")
