import json
import os
from random import random, shuffle

from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import requests

load_dotenv()

blob_service_client = BlobServiceClient.from_connection_string(
    os.getenv("AZURE_STORAGE_CONNECTION_STRING")
)

container_name = os.environ["CONTAINER_NAME"]


batch = 500


def main():
    with open("D:/tmp/newstory/followers.json", "r") as fp:
        followers = json.load(fp)
    profiles = []
    with open("D:/tmp/newstory/labeled_groups.txt", "r") as fp:
        for group in fp.readlines():
            profiles += followers.get(group.strip(), {}).get("data", {}).get("followers", [])
    profiles = [p.strip() for p in profiles]
    existing = list(
        b.name.split("/")[-2]
        for b in blob_service_client.get_container_client(container_name).list_blobs(
            name_starts_with="profiles/2020-11"
        )
    )
    to_scrape = list(set(profiles) - set(existing))
    assert len(profiles) > len(to_scrape)
    shuffle(to_scrape)
    for user in to_scrape:
        print(f"sending {user}")
        res = requests.post(
            f"http://localhost:3030/queue/tasks.profile", json={"args": [user]}
        )
        res.raise_for_status()


if __name__ == "__main__":
    main()
