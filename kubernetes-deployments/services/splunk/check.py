import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import splunklib.client as client

HOST = "splunk-charles-management.us-west1-a.securethebox.us"
PORT = 8089
USERNAME = "admin"
PASSWORD = "Changeme"

service = client.connect(
    scheme="http",
    cookie=1,
    version=7.2,
    host=HOST,
    port=80,
    username=USERNAME,
    password=PASSWORD)

for app in service.apps:
    print(app.name)