import os
import boto3
import glob
import re

from typing import List
from langchain.docstore.document import Document


def extract_from_s3(
    S3_BUCKET_NAME,
    S3_BUCKET_PREFIX,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    DATASET_ROOT_PATH,
) -> None:
    """
    Extracts files from an S3 bucket and saves them to a local path.

    Parameters:
    - S3_BUCKET_NAME: Name of the S3 bucket.
    - S3_BUCKET_PREFIX: Prefix of the S3 path to fetch files.
    - AWS_ACCESS_KEY_ID: AWS Access Key ID.
    - AWS_SECRET_ACCESS_KEY: AWS Secret Access Key.
    - DATASET_ROOT_PATH: Local path to save the downloaded files.

    Returns:
    - None
    """
    # Checking if the path exists
    if not os.path.exists(DATASET_ROOT_PATH):
        os.makedirs(DATASET_ROOT_PATH)

    # Checking if the pdf files had not been downloaded yet
    if len(glob.glob(f"{DATASET_ROOT_PATH}/*.pdf")) == 0:
        # Initialize the S3 client
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        # List objects within the specified prefix
        objects = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=S3_BUCKET_PREFIX)

        print(
            f"Downloading files from s3://{S3_BUCKET_NAME}/{S3_BUCKET_PREFIX} to {DATASET_ROOT_PATH} ..."
        )

        if not os.path.exists(DATASET_ROOT_PATH):
            os.makedirs(DATASET_ROOT_PATH)

        for obj in objects.get("Contents", []):
            # Construct the local file path to mirror the S3 object key structure
            relative_path = obj["Key"][len(S3_BUCKET_PREFIX) :].lstrip("/")
            file_path = os.path.join(DATASET_ROOT_PATH, relative_path)
            # If the S3 object key ends with '/', it's typically a directory, so skip
            if file_path.endswith("/"):
                continue

            # Ensure the directory exists
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Download the object and save it to the local file path
            s3.download_file(S3_BUCKET_NAME, obj["Key"], file_path)
            print(f"Downloaded {obj['Key']} to {file_path}")

        print(
            f"Files from {S3_BUCKET_NAME}/{S3_BUCKET_PREFIX} downloaded to {DATASET_ROOT_PATH}."
        )
    else:
        print(
            f"Files from {S3_BUCKET_NAME}/{S3_BUCKET_PREFIX} already downloaded to {DATASET_ROOT_PATH}."
        )


def preprocess(documents: List[Document]) -> List[Document]:
    """
    This function removes all the extra spaces and new lines from the text.

    Parameters:
    - documents: List of Document objects.

    Returns:
    - documents: List of Document objects.

    """
    for page in documents:
        page.page_content = re.sub(r"(\n\s*){2,}", "\n", page.page_content)
    return documents
