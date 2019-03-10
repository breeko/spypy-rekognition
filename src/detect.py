from config import s3_client, s3_bucket, rekognition_client
from utils import download_to_s3, delete_from_s3

def detect_from_urls(urls):
    if type(urls) is str:
        urls = [urls]

    out = []
    for url in urls:
        image_name = download_to_s3(s3_client, s3_bucket, url)
        image_s3 = {'S3Object': {'Bucket': s3_bucket,'Name': image_name}}
        response = rekognition_client.detect_labels(Image=image_s3, MaxLabels=10)
        delete_from_s3(s3_client, s3_bucket, image_name)
        out.append(response)
    return out
