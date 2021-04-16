import os
from configparser import SafeConfigParser

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def get_config():
    parser = SafeConfigParser(os.environ)
    parser.read_file(open(os.path.join(os.path.dirname(__file__), "newstory.cfg")))
    return parser
