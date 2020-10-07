from concurrent.futures.thread import ThreadPoolExecutor
import json
import os
from typing import List

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import pandas as pd
from tqdm import tqdm

load_dotenv()

blob_service_client = BlobServiceClient.from_connection_string(
    os.getenv("AZURE_STORAGE_CONNECTION_STRING")
)


container_name = os.environ["CONTAINER_NAME"]


def read_blob(blob):
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob)
    download_stream = blob_client.download_blob()
    return download_stream.readall()


def main():
    blobs = list(
        b.name
        for b in blob_service_client.get_container_client(container_name).list_blobs(
            name_starts_with="profiles/2020-10-07/"
        )
    )

    bar = tqdm(total=len(blobs))

    def f(blob):
        res = json.loads(read_blob(blob))
        bar.update()
        return res

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
        profiles: List[dict] = list(pool.map(f, blobs))
    df = pd.DataFrame(
        index=[p["data"]["GraphProfileInfo"]["username"] for p in profiles]
    )
    df["פרטי"] = [p["data"]["GraphProfileInfo"]["info"]["is_private"] for p in profiles]
    df["קישור לפרופיל"] = "https://instagram.com/" + df.index.to_series()
    df["תאריך משיכה"] = [p["created_at"] for p in profiles]
    df["שנת לידה משוערת"] = ""
    df = df.rename_axis("שם משתמש")
    df = df.sort_values("תאריך משיכה")
    df.to_excel("D:/tmp/dob.xlsx", engine="xlsxwriter")


if __name__ == "__main__":
    main()
