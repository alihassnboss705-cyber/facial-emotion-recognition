"""API ko photo bhejo (server pehle chalao).
Istemal:  python test_client.py photo.jpg"""
import sys

import requests

url = "http://127.0.0.1:8000/predict"
with open(sys.argv[1], "rb") as f:
    r = requests.post(url, files={"file": f})
print(r.status_code)
print(r.json())
