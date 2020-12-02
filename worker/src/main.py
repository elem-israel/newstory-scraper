import logging
import traceback

from . import consumers
from .tasks import tasks

logger = logging.getLogger(__name__)


def main(topic):
    logger.info(f"listening to: {topic}")
    for event in consumers[topic]:
        try:
            tasks.get(event.topic)(event)
        except:
            logger.error(traceback.format_exc())
