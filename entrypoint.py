from datetime import datetime
import logging
import sys
from time import sleep
import traceback

from main import main

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

if __name__ == "__main__":
    print("starting")
    start = datetime.now()
    while (datetime.now() - start).total_seconds() < 120:
        try:
            main()
        except:
            traceback.print_exc()
            sleep(5)
            print("retrying...")
    exit(1)
