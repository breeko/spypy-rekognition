import boto3
import requests

from urllib.parse import urlparse
import os
import urllib.request
import shutil

# Download the file from `url` and save it locally under `file_name`:
def download_url(url, file_name):
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return file_name

def get_image_name_from_url(url):
    a = urlparse(url)
    return os.path.basename(a.path)

def download_to_s3(s3_client, s3_bucket, url):
    if not bucket_exists(s3_client, s3_bucket):
        s3_client.create_bucket(Bucket=s3_bucket)

    image_name = get_image_name_from_url(url)
    image = download_url(url, "/tmp/{}".format(image_name))
    s3_client.upload_file(image, s3_bucket, image_name)
    return {'S3Object': {'Bucket': s3_bucket,'Name': image_name}}

def delete_from_s3(s3_client, s3_bucket, file_name):
    s3_client.delete_object(Bucket=s3_bucket, Key=file_name)

def bucket_exists(s3_client, s3_bucket):
    return s3_bucket in [b.get("Name") for b in s3_client.list_buckets().get("Buckets")]