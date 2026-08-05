import os

import razorpay
from dotenv import load_dotenv

load_dotenv()

client = razorpay.Client(
    auth=(os.environ.get("RAZORPAY_KEY_ID"), os.environ.get("RAZORPAY_KEY_SECRET"))
)
