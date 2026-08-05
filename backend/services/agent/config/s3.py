import os
import boto3
from dotenv import load_dotenv
from botocore.config import Config
# Load environment variables from .env
load_dotenv()


s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    endpoint_url=f"https://s3.{os.getenv('AWS_REGION')}.amazonaws.com",
    config=Config(signature_version="s3v4"),
)