import boto3
from decouple import config

aws_access_key = config('aws_key')
aws_secret_key= config('aws_secret')


s3_client = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key

    )