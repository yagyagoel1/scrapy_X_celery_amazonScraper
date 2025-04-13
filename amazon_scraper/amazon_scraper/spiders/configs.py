from dotenv import load_dotenv
import boto3
import os
load_dotenv()
API_KEY = os.getenv('API_KEY')
aws_config= {
    "aws_access_key_id":os.getenv("AWS_ACCESS_KEY"),
    "aws_secret_access_key":os.getenv("AWS_SECRET_KEY")
}

client  = boto3.client("s3",**aws_config)