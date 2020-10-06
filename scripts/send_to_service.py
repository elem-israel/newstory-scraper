import os

from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import requests

load_dotenv()

blob_service_client = BlobServiceClient.from_connection_string(
    os.getenv("AZURE_STORAGE_CONNECTION_STRING")
)

container_name = os.environ["CONTAINER_NAME"]


def main():
    with open("D:/tmp/newstory/youth.txt", "r") as fp:
        profiles = fp.readlines()
    profiles = [p.strip() for p in profiles]
    existing = list(
        b.name.split("/")[1]
        for b in blob_service_client.get_container_client(container_name).list_blobs(
            name_starts_with="profiles/"
        )
    )
    print(existing)
    to_scrape = list(set(profiles) - set(existing))
    assert len(profiles) > len(to_scrape)
    for user in to_scrape[:500]:
        print(f"sending {user}")
        res = requests.get(f"http://localhost:3000/scrape/{user}")
        res.raise_for_status()


if __name__ == "__main__":
    main()
