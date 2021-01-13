import os

import pandas as pd
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
    for d in pd.date_range("2020-09-01", "2020-11-30", freq="D"):
        for blob in blob_service_client.get_container_client(container_name).list_blobs(
            name_starts_with=f"profiles/{d.strftime('%Y-%m-%d')}"
        ):
            print(f"sending {blob.name}")
            res = requests.post(
                f"http://localhost:3030/queue/newstory.tasks.newEntry",
                json={"message": blob.name},
            )
            res.raise_for_status()


if __name__ == "__main__":
    main()
