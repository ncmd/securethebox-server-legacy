import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import splunklib.client as client

HOST = "splunk-charles.us-west1-a.securethebox.us"
PORT = 8089
USERNAME = "admin"
PASSWORD = "Changeme"

service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD)

for app in service.apps:
    print(app.name)