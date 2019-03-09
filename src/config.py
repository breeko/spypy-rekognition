import boto3

s3_bucket = "spypy-images"

rekognition_client=boto3.client('rekognition')
s3_client=boto3.client('s3')