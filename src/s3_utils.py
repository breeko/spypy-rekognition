import os
import urllib.request
import json
from typing import List

FilePaths = List[str]
FileNames = List[str]

def upload_dictionary_to_s3(s3_client, s3_bucket, file_name, d) -> FilePaths:
    """ Uploads a dictionary to s3 

    Inputs:
        s3_client (botocore.client.S3)
        s3_bucket (str)
        file_name (str)
        d (dictionary)
    Outputs:
        file_name (str): name of the json that was uploaded
    """
    json_file = file_name if file_name.endswith(".json") else "{}.json".format(file_name)
    out_path = os.path.join("/tmp", json_file)
    with open(out_path, 'w') as f:
        json.dump(d, f)
    out = upload_files_to_s3(s3_client, s3_bucket, out_path)
    os.remove(out_path)
    return out

def upload_files_to_s3(s3_client, s3_bucket, files_or_urls) -> FilePaths:
    """ Uploads a local image or url to an s3 bucket 
    
    Inputs:
        s3_client (boto.client.S3)
        s3_bucket (str)
        files_or_urls ([str]):                   Either a path to a local file or url prepended with http
    Outputs:
        file_names ([str]):                     Name of the uploaded file
    """
    if not s3_bucket_exists(s3_client, s3_bucket):
        s3_client.create_bucket(Bucket=s3_bucket)

    if type(files_or_urls) is not list:
        files_or_urls = [files_or_urls]

    file_names = []
    for file_or_url in files_or_urls:
        if file_or_url.startswith("http"):
            file_name = download_url(file_or_url)
            file_path = file_name
            url=True
        else:
            file_path = file_or_url
            file_name = file_or_url.split("/")[-1]
            url=False
        
        if not s3_file_exists(s3_client, s3_bucket, file_name):
            s3_client.upload_file(file_path, s3_bucket, file_name)
        file_names.append(file_name)
    return file_names

def get_s3_file_names(s3_client, s3_bucket: str) -> FileNames:
    """ Returns file names from s3 bucket 

    Inputs:
        s3_client (boto.client.S3)
        s3_bucket (str)
    Outputs:
        file_names (list):           List of file names from the bucket
    """
    s3_objects = s3_client.list_objects(Bucket=s3_bucket)
    s3_contents = s3_objects["Contents"]
    s3_files = [content["Key"] for content in s3_contents]
    return s3_files
    
def delete_from_s3(s3_client, s3_bucket, file_names) -> FileNames:
    """ Deletes a file from an s3 bucket """
    if type(file_names) is not list:
        file_names = [file_names]
    
    for file_name in file_names:
        s3_client.delete_object(Bucket=s3_bucket, Key=file_name)
    return file_names

def s3_bucket_exists(s3_client, s3_bucket) -> bool:
    """ Returns whether a bucket exists 

    Inputs:
        s3_client (boto.client.S3)
        s3_bucket (str)
    Outputs:
        file_exists (bool)
    """
    return s3_bucket in [b.get("Key") for b in s3_client.list_buckets().get("Buckets")]

def s3_file_exists(s3_client, s3_bucket, file_name) -> bool:
    """ Returns whether a file exists in a bucket 
    Inputs:
        s3_client (boto.client.S3)
        s3_bucket (str)
        file_name (str)
    Outputs:
        file_exists (bool)
    """
    try:
        s3_client.get_object(Bucket=s3_bucket, Key=file_name)
        return True
    except:
        return False

def download_files_from_s3(s3_client, s3_bucket, files, path) -> FilePaths:
    """ Downloads files from s3 bucket to given directory """
    if type(files) is not list:
        files = [files]
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    out = []
    for f in files:
        out_path = os.path.join(path, f)
        s3_client.download_file(s3_bucket, f, out_path)
        out.append(out_path)

    return out