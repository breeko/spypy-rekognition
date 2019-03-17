import json
from typing import List
import config
import datetime as dt
import time

def json_to_human_time(json_file: str) -> str:
    file_name = json_file.replace(".json", "")

    utc = dt.datetime.strptime(file_name, config.date_format)
    local = utc_to_local(utc)
    local_printable = local.strftime(config.date_format_printable)
    
    return local_printable

def utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = dt.datetime.fromtimestamp(now_timestamp) - dt.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

def read_json_paths(paths: List[str]) -> List[dict]:
    out = []
    for file_path in paths:
        if file_path.endswith(".json"):
            with open(file_path) as f:
                out.append(json.load(f))
    return out
