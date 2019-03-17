source env/bin/activate
cd src

python -c \
"""
from static import s3_client, rekognition_client
from s3_utils import upload_files_to_s3
from PIL import Image
from convert import draw_boxes, get_bounding_boxes

image_path='../images/warehouse/2019-03-14-20-0-0-0.png'
image_name = upload_files_to_s3(s3_client, 'spypy-test', image_path)[0]
image = Image.open(image_path)
print(image_name)
image_s3 = {'S3Object': {'Bucket': 'spypy-test','Name': image_name}}
response = rekognition_client.detect_labels(Image=image_s3, MaxLabels=10)

bounding_boxes = get_bounding_boxes(
    replies=response,
    image_height=image.height,
    image_width=image.width,
    min_confidence=0.5
)
image = draw_boxes(image, bounding_boxes)
image.show()
"""

