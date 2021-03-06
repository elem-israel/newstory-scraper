import json_logging

json_logging.init_logger()

import logging
import os
import sys
import traceback
from time import sleep

import kafka.errors

from kafka_config import get_consumer, get_producer
from tasks import echo, insert_to_db, upload, scrape_profile


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

topic_to_task = {
    "newstory.tasks.newentry": insert_to_db.insert_to_db,
    "newstory.tasks.echo": echo.echo,
    "newstory.tasks.upload": upload.upload,
    "newstory.tasks.scrape": scrape_profile.scrape_profile,
}


bootstrap_servers = [
    f'{os.getenv("KAFKA_HOST", "localhost")}:{os.getenv("KAFKA_PORT", "9092")}'
]


def main():
    logger.info("connecting to kafka: {}".format(",".join(bootstrap_servers)))
    while True:
        try:
            producer = get_producer(bootstrap_servers)
            logger.info(f"listening to: {os.environ['KAFKA_TOPICS_LISTENER']}")
            for event in get_consumer(
                os.environ["KAFKA_TOPICS_LISTENER"].split(","),
                bootstrap_servers,
            ):
                logger.info(f"received event, {event}")
                try:
                    topic_to_task.get(event.topic)(event.value)
                except:
                    logger.error(traceback.format_exc())
                    producer.send(
                        topic="newstory.deadletter",
                        key="event.topic",
                        value={"event": event, "stack": traceback.format_exc()},
                    )
        except kafka.errors.NoBrokersAvailable as e:
            logger.warning(e)
            sleep(5)


if __name__ == "__main__":
    main()
