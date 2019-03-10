import boto3
import requests

from urllib.parse import urlparse
import os
import urllib.request
import shutil

def download_url(url):
    """ Downloads a url and returns the file path """
    file_name = get_image_name_from_url(url)
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return file_name

def get_image_name_from_url(url):
    """ Returns the file path of a url """
    a = urlparse(url)
    return os.path.basename(a.path)

def download_to_s3(s3_client, s3_bucket, url, keep=False):
    """ Downloads a url to an s3 bucket """
    if not bucket_exists(s3_client, s3_bucket):
        s3_client.create_bucket(Bucket=s3_bucket)

    image_name = download_url(url)
    s3_client.upload_file(image_name, s3_bucket, image_name)
    if not keep:
        os.remove(image_name)
    return image_name

def delete_from_s3(s3_client, s3_bucket, file_name):
    """ Deletes a file from an s3 bucket """
    s3_client.delete_object(Bucket=s3_bucket, Key=file_name)

def bucket_exists(s3_client, s3_bucket):
    """ Returns whether a bucket exists """
    return s3_bucket in [b.get("Name") for b in s3_client.list_buckets().get("Buckets")]