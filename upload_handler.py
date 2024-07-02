import logging
from flask import request, jsonify
from azure.storage.blob import BlobServiceClient
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Get Azure Blob Storage configuration from environment variables
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

# Log environment variables for debugging
logging.debug(f"Connection String: {connect_str}")
logging.debug(f"Container Name: {container_name}")


def upload():
    try:
        # Check if environment variables are set
        if not connect_str or not container_name:
            raise ValueError("Azure Storage connection string or container name not set")

        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Get container client
        container_client = blob_service_client.get_container_client(container_name)

        files = request.files.getlist('files')
        logging.debug(f"Files received: {files}")

        for file in files:
            logging.debug(f"Uploading file: {file.filename}")
            # Create a blob client using the local file name as the name for the blob
            blob_client = container_client.get_blob_client(file.filename)

            # Upload the created file
            blob_client.upload_blob(file)
            logging.debug(f"File {file.filename} uploaded successfully")

        return jsonify({"message": "Files uploaded successfully"}), 200

    except Exception as e:
        logging.error("Error uploading file: %s", e)
        return jsonify({"error": str(e)}), 500
