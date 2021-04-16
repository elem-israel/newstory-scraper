import json
import logging
import os
from datetime import date
from datetime import datetime

from newstory_scraper.util import extract_posts
from newstory_scraper.util import extract_tags
from newstory_scraper.util import traverse_path

logger = logging.getLogger(__name__)


def normalize_item(path):
    data = json.load(open(path))
    hashtags = extract_tags(data)
    posts = extract_posts(data)
    return {"hashtags": hashtags, "posts": posts}


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def transform(source, target):
    for item in list(traverse_path(source)):
        res = normalize_item(item)
        target_item = item.replace(source, target)
        os.makedirs(os.path.dirname(target_item), exist_ok=True)
        json.dump(res, open(target_item, "w"), default=json_serial, indent=2)
    print(target)
