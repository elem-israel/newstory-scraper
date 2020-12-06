import logging
import os
import traceback
from . import tasks, consumer, producer

logger = logging.getLogger(__name__)

topic_to_task = {
    "newstory.tasks.newEntry": tasks.insert_to_db,
    "newstory.tasks.echo": tasks.echo,
    "newstory.tasks.upload": tasks.upload,
}


def main():
    logger.info(f"listening to: {os.environ['KAFKA_TOPICS_LISTENER']}")
    for event in consumer:
        logger.info(f"received event, {event}")
        try:
            topic_to_task.get(event.topic)(event.value)
        except:
            logger.error(traceback.format_exc())
            producer.send(
                "newstory.deadLetter",
                value={"event": event, "stack": traceback.format_exc()},
            )
