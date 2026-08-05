import os
import json
import firebase_admin
from firebase_admin import credentials

service_account_info = json.loads(
    os.environ["FIREBASE_SERVICE_ACCOUNT_JSON"]
)

cred = credentials.Certificate(service_account_info)

app = firebase_admin.initialize_app(cred)