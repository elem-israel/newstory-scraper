import os

import requests


def main():
    with open("D:/tmp/newstory/youth.txt", "r") as fp:
        profiles = fp.readlines()
    profiles = [p.strip() for p in profiles]
    existing = os.listdir("D:/tmp/newstory/profiles")
    existing = []
    to_scrape = list(set(profiles) - set(existing))
    assert len(profiles) > len(to_scrape)
    for user in to_scrape[1000:1500]:
        print(f"sending {user}")
        res = requests.get(f"http://localhost:3000/scrape/{user}")
        res.raise_for_status()


if __name__ == "__main__":
    main()
