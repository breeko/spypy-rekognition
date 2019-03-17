source env/bin/activate
cd src
python -c \
"""
from handler import process_image
event = { 'Records': [ { 's3': { 'bucket': {'name': 'spypy-test'}, 'object': {'key': '2019-03-14-20-0-0-0.png'} } } ] }
out = process_image(event, None)
print(out)
"""