import os
from dotenv import load_dotenv

from config.s3 import s3_client


load_dotenv()

def get_from_s3(file_name: str, expires_in: int = 600) -> str:
    """
    Generate a pre-signed URL for downloading an object from S3.

    Args:
        file_name: S3 object key.
        expires_in: URL expiration time in seconds (default: 600).

    Returns:
        A pre-signed URL.
    """
    

    url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": os.getenv("AWS_BUCKET_NAME"),
            "Key": file_name,
        },
        ExpiresIn=expires_in,
    )
    print(url)
    return url