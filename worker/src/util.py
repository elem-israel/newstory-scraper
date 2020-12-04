import os
import jsonpath_ng


def read_blob(client, container_name, blob):
    container_client = client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob)
    download_stream = blob_client.download_blob()
    return download_stream.readall()


def get_bool_from_env(key):
    return os.getenv(key) in ["True", "true", "1", "yes"]


def extract_profile(dictionary):
    return {
        "created_at": extract_jsonpath("$.created_at", dictionary)[0],
        "username": extract_jsonpath("$.data.GraphProfileInfo.username", dictionary)[0],
        **extract_jsonpath("$.data.GraphProfileInfo.info", dictionary)[0],
    }


def extract_jsonpath(expression, dictionary):
    jsonpath_expr = jsonpath_ng.parse(expression)
    return [v.value for v in jsonpath_expr.find(dictionary)]
