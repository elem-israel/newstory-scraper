import logging
import os
import traceback
from kafka_config import get_consumer, get_producer
from tasks import echo, insert_to_db, upload

logger = logging.getLogger(__name__)

topic_to_task = {
    "newstory.tasks.newEntry": insert_to_db.insert_to_db,
    "newstory.tasks.echo": echo.echo,
    "newstory.tasks.upload": upload.upload,
}


def main():
    producer = get_producer()
    logger.info(f"listening to: {os.environ['KAFKA_TOPICS_LISTENER']}")
    for event in get_consumer():
        logger.info(f"received event, {event}")
        try:
            topic_to_task.get(event.topic)(event.value)
        except:
            logger.error(traceback.format_exc())
            producer.send(
                "newstory.deadLetter",
                value={"event": event, "stack": traceback.format_exc()},
            )
