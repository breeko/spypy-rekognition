from PIL import ImageDraw, ImageFont, Image
from static import *
from s3_utils import *
from utils import read_json_paths
from image_utils import get_median_image
import config
from utils import json_to_human_time

def get_bounding_boxes(replies, image_height, image_width, min_confidence):
    """ Processes and flattens rekognition replies 
    input:
        replies ([dict]):           list of rekognition replies
        image_height (float):       height of the image used to scale boxes
        image_width (float):        width of the image used to scale boxes
        min_confidence (float):     minimum confidence to  be considered a match
    output:
        out (dict):                 a flat list of objects detected
    e.g.
    [{"name": "person", "left": 100.0, "top": 50.0, "width": 200.0, "height": 150.0 }, ...]
    """
    if type(replies) is not list:
        replies = [replies]
    
    min_confidence_perc = min_confidence * 100.0

    out = []
    for reply in replies:
        labels = reply.get("Labels", [])
        for label in labels:
            name = label.get("Name")
            instances = label.get("Instances", [])
            for instance in instances:
                box = instance.get("BoundingBox")
                confidence = instance.get("Confidence", 0)
                if box and confidence > min_confidence_perc:
                    left = box['Left'] * image_width
                    top = box['Top'] * image_height
                    width = box['Width'] * image_width
                    height = box['Height'] * image_height
                    out.append({"name": name, "left": left, "top": top, "width": width, "height": height})
    return out


def draw_boxes(image, bounding_boxes, color=(255,0,0), title=None, fill_alpha=None):
    """ Returns the labels and instances with a bounding box 
    
    input:
        image (PIL Image):          image to be drawn over
        bounding_boxes (list):      list of dictionaries to draw, containing name, left, top, width and height
        fill_alpha (int):         alpha to use when filling bounding boxes
    output:
        out (list):             list of objects
    """
    if type(bounding_boxes) is not list:
        bounding_boxes = [bounding_boxes]
    
    image_width, image_height = image.size
    font_size = min(image_width, image_height) // 20
    font = ImageFont.truetype("fonts/calibri.ttf", font_size)

    if fill_alpha:
        image = image.convert("RGB")
        tmp_draw = ImageDraw.Draw(image, "RGBA")
        tmp_fill = (*color, fill_alpha)
    else:
        tmp_draw = ImageDraw.Draw(image)
    
    for box in bounding_boxes:
        name = box["name"]
        left = box["left"]
        top = box["top"]
        width = box["width"]
        height = box["height"]
        
        if fill_alpha:
            tmp_draw.rectangle(((left, top), (left + width, top + height)), fill=tmp_fill)
        else:
            tmp_draw.rectangle([left, top, left + width, top + height], outline=color, width=2) 
            tmp_draw.text((left+1, top), name, font=font, fill="black")
            tmp_draw.text((left-1, top), name, font=font, fill="black")
            tmp_draw.text((left, top+1), name, font=font, fill="black")
            tmp_draw.text((left, top-1), name, font=font, fill="black")
            tmp_draw.text((left, top), name, font=font, fill="white")

    if title:
        left = 10
        top = 10
        tmp_draw.text((left+1, top), title, font=font, fill="black")
        tmp_draw.text((left-1, top), title, font=font, fill="black")
        tmp_draw.text((left, top+1), title, font=font, fill="black")
        tmp_draw.text((left, top-1), title, font=font, fill="black")
        tmp_draw.text((left, top), title, font=font, fill="white")

    return image

def get_heatmap(processed_bucket, unprocessed_bucket, file_filter, object_match, min_confidence, fill_alpha):
    """ 
    Returns a heatmap of an object in a group of images

    Inputs:
        processed_bucket (str):                 name of the bucket containing the processed images
        unprocessed_bucket (str):               name of the bucket containing the unprocessed images
        file_filter (lambda: [str] -> [str]):   filter to apply to files in a bucket
        object_match (str):                     object to search for
        min_confidence (float):                 minimum confidence to consider a match
        fill_alpha (int):                       amount of alpha to provide each detection
    Outputs:
        out (dictionary):                       representation of detections in a set of processed images

    """
    processed_files = get_s3_file_names(s3_client, processed_bucket)
    unprocessed_files = get_s3_file_names(s3_client, unprocessed_bucket)
    
    processed_files_filtered = file_filter(processed_files)
    unprocessed_files_filtered = file_filter(unprocessed_files)

    unprocessed_paths = download_files_from_s3(
        s3_client, config.s3_unprocessed_bucket, unprocessed_files_filtered, "/tmp/unprocessed")
    processed_paths = download_files_from_s3(
        s3_client, config.s3_processed_bucket, processed_files_filtered, "/tmp/processed")

    image = get_median_image(unprocessed_paths)
    replies = read_json_paths(processed_paths)

    bounding_boxes = get_bounding_boxes(
        replies=replies, image_height=image.height, image_width=image.width, min_confidence=min_confidence)
    
    bounding_boxes_filtered = [b for b in bounding_boxes if b.get("name").lower() == object_match]

    # TODO: determine good alpha
    out = draw_boxes(image, bounding_boxes_filtered, title=object_match, fill_alpha=fill_alpha)
    return out

def get_report(processed_bucket, file_filter, object_match, min_confidence):
    """ 
    Returns a report based on a bucket containing processed files

    Inputs:
        processed_bucket (str):                 name of the bucket containing the processed images
        file_filter (lambda: [str] -> [str]):   filter to apply to files in a bucket
        min_confidence (float):                 minimum confidence to consider a match
    Outputs:
        out (dictionary):                       representation of detections in a set of processed images

    e.g.

    {num_frames: 2,
        start: "...",
        stop: "...",
        objects: {
            person: {
                max: 2, 
                min: 1,
                mean: 1.5,
                median: 1.5,
                frames_present: 2 
            }, 
            cat: {...}
        }
    }
    """
    processed_files = get_s3_file_names(s3_client, processed_bucket)
    processed_files_filtered = file_filter(processed_files)

    json_to_readable_date = lambda j: dt.datetimej.replace(".json", "")
    first = json_to_human_time(min(processed_files_filtered))
    last = json_to_human_time(max(processed_files_filtered))
    
    processed_paths = download_files_from_s3(
        s3_client, config.s3_processed_bucket, processed_files_filtered, "/tmp/processed")

    replies = read_json_paths(processed_paths)

    frames = []
    all_names = [object_match]

    for reply in replies:
        boxes = get_bounding_boxes(replies=reply, image_height=1, image_width=1, min_confidence=min_confidence) # only used to unpack
        frame = {}
        for box in boxes:
            name = box.get("name").lower()
            frame[name] = frame.get(name, 0) + 1
        frames.append(frame)
    
    objects = {name: {} for name in all_names}
    num_frames = len(frames)

    for frame in frames:        
        for name, count in frame.items():
            if name == object_match:
                cur_object = objects.get(name)
                new_max = max(cur_object.get("max", -float("inf")), count)

                new_min = min(cur_object.get("min", float("inf")), count)
                new_total = cur_object.get("total", 0) + count
                new_frames_present = cur_object.get("frames_present", 0) + 1
                
                new_object = {"max": new_max, "min": new_min, "total": new_total, "frames_present": new_frames_present}
                objects[name] = new_object
    
    objects = {key: {**val, "mean": val.get("total", 0.0) / num_frames, "perc_present": val.get("frames_present") / num_frames} for key, val in objects.items()}

    summary = {
        "num_frames": num_frames,
        "first": first,
        "last": last,
        "objects": objects
    }

    return summary 
