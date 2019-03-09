from config import s3_client, s3_bucket, rekognition_client
from utils import download_to_s3, delete_from_s3

def detect_images_from_urls(urls):
    if type(urls) is str:
        urls = [urls]

    out = []
    for url in urls:
        image = download_to_s3(s3_client, s3_bucket, url)
        response = rekognition_client.detect_labels(Image=image, MaxLabels=10)
        delete_from_s3(s3_client, s3_bucket, image.get("S3Object").get("Name"))
        out.append(response)
    return out
