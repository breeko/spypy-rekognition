source env/bin/activate
cd src

python -c \
"""
from config import s3_client, s3_bucket, rekognition_client
from utils import download_to_s3
from PIL import Image
from convert import draw_boxes

url='https://ferguspigeonman.files.wordpress.com/2012/04/img_6828.jpg'

image_name = download_to_s3(s3_client, s3_bucket, url, keep=True)
image_s3 = {'S3Object': {'Bucket': s3_bucket,'Name': image_name}}
im = Image.open(image_name)
replies = rekognition_client.detect_labels(Image=image_s3, MaxLabels=10)
im = draw_boxes(im, replies)
im.show()
"""

