source env/bin/activate
cd src
python -c \
"""
from handler import summary
import json

report = summary({'t': 'report', 'h': 12}, {})
print(json.dumps(report, indent=2))

im = summary({'t': 'heatmap', 'h': 12, 'a': 20}, {})
"""
