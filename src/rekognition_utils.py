
def get_bounding_boxes(replies, image_height, image_width, min_confidence=0.5):
    if type(replies) is not list:
        replies = [replies]
    
    out = []
    for reply in replies:
        labels = reply.get("Labels", [])
        for label in labels:
            name = label.get("Name")
            instances = label.get("Instances", [])
            for instance in instances:
                box = instance.get("BoundingBox")
                confidence = instance.get("Confidence", 0)
                if box and confidence > 0.5:
                    left = box['Left'] * image_width
                    top = box['Top'] * image_height
                    width = box['Width'] * image_width
                    height = box['Height'] * image_height
                    out.append({"name": name, "left": left, "top": top, "width": width, "height": height})
    return out

