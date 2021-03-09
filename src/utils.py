from azure.storage.blob import BlobServiceClient


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
