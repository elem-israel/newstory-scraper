import logging
import sys
from datetime import datetime
from decimal import Decimal

from pythonjsonlogger import jsonlogger


def EncodeDecimal(o):
    if isinstance(o, Decimal):
        return float(round(float(o), 8))
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")


def getLogger(*args, **kwargs):
    logger = logging.getLogger(*args, **kwargs)
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(levelname)s %(name)s %(message)s", json_default=EncodeDecimal, timestamp=True
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
