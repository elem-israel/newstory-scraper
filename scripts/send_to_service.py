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
    blobs = list(
        blob_service_client.get_container_client(container_name).list_blobs(
            name_starts_with="profiles/2020-11"
        )
    )
    # remove duplicates
    profiles = {b.name.split("/")[-2]: b for b in blobs}
    for blob in profiles.values():
        print(f"sending {blob}")
        res = requests.post(
            f"http://localhost:3030/queue/newstory.tasks.newEntry",
            json={"message": blob.name},
        )
        res.raise_for_status()


if __name__ == "__main__":
    main()
