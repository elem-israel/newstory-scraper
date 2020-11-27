import sys

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from src.main import main

if __name__ == "__main__":
    main(sys.argv[1])
