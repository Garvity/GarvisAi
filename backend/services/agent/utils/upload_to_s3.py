import os
from dotenv import load_dotenv

from config.s3 import s3_client

load_dotenv()


def upload_to_s3(file_name: str, buffer: bytes, content_type: str) -> str:
    """
    Upload a file to an S3 bucket.

    Args:
        file_name: Name/key of the object in S3.
        buffer: File contents as bytes.
        content_type: MIME type (e.g., image/png, application/pdf).

    Returns:
        The uploaded file name (S3 object key).
    """

    s3_client.put_object(
        Bucket=os.getenv("AWS_BUCKET_NAME"),
        Key=file_name,
        Body=buffer,
        ContentType=content_type,
    )

    return file_name