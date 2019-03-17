from s3_utils import *
from static import *
from convert import *
import config
from image_utils import filter_files_by_time, get_median_image
import base64
from io import BytesIO


def process_image(event: dict, context: dict) -> dict:
    """ Processes the image placed into a bucket """
    image_name = event['Records'][0]['s3']['object']['key']
    s3_unprocessed_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_processed_bucket = "{}-objects-processed".format(s3_unprocessed_bucket)    

    image_s3 = {'S3Object': {'Bucket': s3_unprocessed_bucket, 'Name': image_name}}
    response = rekognition_client.detect_labels(Image=image_s3, MaxLabels=config.max_labels)
    upload_dictionary_to_s3(s3_client, s3_processed_bucket, image_name, response)
    
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": { },
        "body": str(response)
    }

def summary(event: dict, context: dict) -> dict:
    """ Returns a processed representation of the saved snapshots """
    
    string_params = event.get("queryStringParameters") or {}
    
    hours_raw = string_params.get("h", 12)
    object_match_raw = string_params.get("o", "person")
    out_raw = string_params.get("t", "report")
    alpha_raw = string_params.get("a", config.alpha)
    confidence_raw = string_params.get("c", config.min_confidence)
    
    hours = float(hours_raw)
    object_match = object_match_raw.lower()
    out_type = out_raw.lower()
    alpha = int(alpha_raw)
    confidence = float(confidence_raw)

    file_filter = lambda f: filter_files_by_time(f, hours)

    if out_type == "report":
        out = get_report(
            processed_bucket=config.s3_processed_bucket,
            file_filter=file_filter,
            object_match=object_match,
            min_confidence=config.min_confidence
            )
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": { },
            "body": str(out)
        }

    elif out_type == "heatmap":
        image = get_heatmap(
            processed_bucket=config.s3_processed_bucket,
            unprocessed_bucket=config.s3_unprocessed_bucket,
            file_filter=file_filter,
            object_match=object_match,
            min_confidence=config.min_confidence,
            fill_alpha = alpha
            )
        
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        encoded_string = base64.b64encode(buffered.getvalue())
        
        return {
            "isBase64Encoded": True,
            "statusCode": 200,
            "headers": {"content-type": "image/png" },
            "body":  encoded_string.decode("utf-8")
        }
    else:
        raise ValueError("Invalid type: {}. Must be either report or heatmap".format(out_type))
    
