from PIL import ImageDraw, ImageFont
from rekognition_utils import get_bounding_boxes

def draw_boxes(image, replies, min_confidence=0.5):
    """ Returns the labels and instances with a bounding box 
    input:
        image (PIL Image):          image to be drawn over
        replies (list):             aws rekognition reply
        min_confidence (float):     minimum confidence to return
    output:
        out (list):             list of objects
    """
    if type(replies) is not list:
        replies = [replies]

    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    font_size = min(image_width, image_height) // 20
    font = ImageFont.truetype("fonts/calibri.ttf", font_size)

    bounding_boxes = get_bounding_boxes(
        replies=replies,
        image_height=image_height,
        image_width=image_width,
        min_confidence=min_confidence
    )
    for box in bounding_boxes:
        name = box["name"]
        left = box["left"]
        top = box["top"]
        width = box["width"]
        height = box["height"]
        
        draw.rectangle([left, top, left + width, top + height], outline='red', width=2) 
        draw.text((left+1, top), name, font=font, fill="black")
        draw.text((left-1, top), name, font=font, fill="black")
        draw.text((left, top+1), name, font=font, fill="black")
        draw.text((left, top-1), name, font=font, fill="black")
        draw.text((left, top), name, font=font, fill="white")
        
    return image