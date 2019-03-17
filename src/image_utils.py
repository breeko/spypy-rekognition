from PIL import Image
import numpy as np
import config
import datetime as dt
from typing import List

def get_median_image(paths: List[str]) -> Image:
    """ Returns the median image from images in a directory 
    Input:
        paths (str):            list of file paths
    Output:
        image (PIL.Image):            image containing the median pixel values
    """
    image_paths = [f for f in paths if f.endswith(config.valid_image_types)]
    images = [Image.open(f) for f in image_paths]
    images_arr = np.array([np.asarray(im) for im in images])
    image_arr_median = np.array(np.median(images_arr, axis=0), dtype=np.uint8)
    image_median = Image.fromarray(image_arr_median)

    return image_median

def filter_files_by_time(all_files: List[str], hours: float = None) -> List[str]:
    if hours:
        latest_time = dt.datetime.utcnow() - dt.timedelta(hours=hours)
    else:
        latest_time = dt.datetime.min
    
    out = []
    for f in all_files:
        try:
            f_no_ext = "".join(f.split(".")[:-1])
            f_time = dt.datetime.strptime(f_no_ext, config.date_format)
            if f_time > latest_time:
                out.append(f)
        except ValueError:
            # not in the correct format
            continue
    return out

