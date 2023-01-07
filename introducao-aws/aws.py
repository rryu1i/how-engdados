#%%
import boto3
from botocore import exceptions
from botocore.exceptions import ClientError
import logging
from dotenv import load_dotenv
from os import getenv

#%%
load_dotenv('/home/roger/.env')

#%%
s3_client = boto3.client(
    's3',
    aws_access_key_id = getenv('AWS_ID'),
    aws_secret_access_key = getenv('AWS_KEY')
)

#%%
def criar_bucket(nome):
    try:
        s3_client.create_bucket(Bucket=nome)
    except ClientError as e:
        logging.error(e)
        return False
    return True
