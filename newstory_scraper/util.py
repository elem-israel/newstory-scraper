import logging
import os
from datetime import datetime
from typing import List
from typing import Union

import jsonpath_ng
import requests
from azure.storage.blob import BlobServiceClient

logger = logging.getLogger(__name__)


def read_blob(client, container_name, blob):
    container_client = client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob)
    download_stream = blob_client.download_blob()
    return download_stream.readall()


def get_bool_from_env(key):
    if os.getenv(key) in ["True", "true", "1", "yes"]:
        return True
    elif os.getenv(key) in ["False", "false", "0", "no"]:
        return False
    else:
        return None


def extract_profile(dictionary):
    extracted = extract_jsonpath("$.data.GraphProfileInfo.info", dictionary)[0]
    return {
        "created_date": datetime.fromisoformat(
            extract_jsonpath("$.created_at", dictionary)[0]
        ),
        "profile_created_at": datetime.utcfromtimestamp(
            extract_jsonpath("$.data.GraphProfileInfo.created_time", dictionary)[0]
        ),
        "username": extract_jsonpath("$.data.GraphProfileInfo.username", dictionary)[0],
        "instagram_profile_id": extracted["id"],
        **{
            k: v
            for k, v in extracted.items()
            if k
            in (
                "username",
                "followers_count",
                "biography",
                "following_count",
                "full_name",
                "is_business_account",
                "is_private",
                "posts_count",
                "profile_pic_url",
            )
        },
    }


def get_from_list(iterable: list, index=0, default=None):
    return (iterable[index : index + 1] or [default])[index]


def extract_posts(dictionary):
    posts = get_from_list(
        extract_jsonpath("$.data.GraphImages", dictionary), default=[]
    )
    posts = [
        {
            "resource": "post",
            "created_date": datetime.fromisoformat(
                extract_jsonpath("$.created_at", dictionary)[0]
            ),
            "taken_at": datetime.utcfromtimestamp(post["taken_at_timestamp"]),
            "instagram_post_id": post["id"],
            "instagram_author_profile_id": extract_jsonpath("$.owner.id", post)[0],
            "caption": get_from_list(
                extract_jsonpath("$.edge_media_to_caption.edges..node.text", post)
            ),
            "likes_count": extract_jsonpath("$.edge_media_preview_like.count", post)[0],
            "image": extract_jsonpath("$.display_url", post)[0],
        }
        for post in posts
    ]
    return posts


def extract_tags(dictionary):
    posts = get_from_list(
        extract_jsonpath("$.data.GraphImages", dictionary), default=[]
    )
    posts = [
        {
            "type": "hashtag",
            "instagram_post_id": post["id"],
            "tags": get_from_list(extract_jsonpath("$.tags", post)),
        }
        for post in posts
    ]
    # post = {instagram_post_id: 123, tags: [tag1, tags2....]}
    tags = [
        [{"instagram_post_id": p["instagram_post_id"], "tag": t} for t in p["tags"]]
        for p in posts
        if p["tags"]
    ]
    # tag = [{instagram_post_id: 123, tag: tag1}, ....]
    return [i for j in tags for i in j]


def extract_jsonpath(expression, dictionary):
    jsonpath_expr = jsonpath_ng.parse(expression)
    return [v.value for v in jsonpath_expr.find(dictionary)]


def get_proxy():
    if os.environ.get("PROXY_USER"):
        super_proxy_url = "http://{}:{}@{}:{}".format(
            os.environ["PROXY_USER"],
            os.environ["PROXY_PASSWORD"],
            os.environ["PROXY_HOST"],
            os.environ["PROXY_PORT"],
        )
        return {"http": super_proxy_url, "https": super_proxy_url}
    else:
        return {}


def get_username_by_id(id: Union[str, int]):
    url = f"https://i.instagram.com/api/v1/users/{id}/info/"
    logger.info("sending request to {}".format(url))
    proxies = get_proxy()
    res = requests.get(
        f"https://i.instagram.com/api/v1/users/{id}/info/",
        headers={
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 Instagram 12.0.0.16.90 (iPhone9,4; iOS 10_3_3; en_US; en-US; scale=2.61; gamut=wide; 1080x1920)"
        },
        proxies=proxies,
        verify=False if len(proxies) else True,
    )
    res.raise_for_status()
    if b"login" in res.content:
        raise ValueError("Login page hit!")
    logger.info("received result: {}".format(res.json()))
    return res.json()["user"]["username"]


def upload_to_azure_storage(
    connect_str, local, container_name, remote, overwrite=False
):
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=remote
    )

    print("\nUploading to Azure Storage as blob:\n\t" + local)

    # Upload the created file
    with open(local, "rb") as data:
        blob_client.upload_blob(data, overwrite=overwrite)


def flatten(list_of_lists: List[list]) -> list:
    """
    flatten a list of lists
    [[a],[b]] -> [a,b]
    :param list_of_lists:
    :return: flat list
    """
    return [item for sublist in list_of_lists for item in sublist]


def traverse_path(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            yield os.path.join(root, filename)
