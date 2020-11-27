import logging
import sys
import traceback

from . import consumers, tasks

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def main(topic):
    logger.info(f"listening to: {topic}")
    for event in consumers.get(topic):
        try:
            getattr(tasks, event.topic)(event)
        except:
            logger.error(traceback.format_exc())
