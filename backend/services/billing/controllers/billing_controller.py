import asyncio
import hashlib
import hmac
import os
import time

import httpx
from fastapi import Request
from fastapi.responses import JSONResponse

from config.plans import PLANS
from config.razorpay_client import client as razorpay_client
from models.payment import Payment, utc_now


async def create_order(request: Request):
    try:
        body = await request.json()
        plan = body.get("plan")
        user_id = request.headers.get("x-user-id")
        selected_plan = PLANS.get(plan)
        if not selected_plan:
            return JSONResponse(status_code=400, content={"message": "Invalid plan"})
        # razorpay SDK is synchronous; run it off the event loop
        order = await asyncio.to_thread(
            razorpay_client.order.create,
            {
                "amount": selected_plan["amount"] * 100,
                "currency": "INR",
                "receipt": f"receipt-{int(time.time() * 1000)}",
            },
        )
        payment = Payment(
            userId=user_id,
            orderId=order["id"],
            amount=selected_plan["amount"],
            credits=selected_plan["credits"],
            plan=selected_plan["id"],
            currency=order["currency"],
            status="created",
        )
        await payment.insert()
        return JSONResponse(
            status_code=200, content={"order": order, "plan": selected_plan}
        )
    except Exception:
        return JSONResponse(
            status_code=500, content={"message": "Internal server error"}
        )


async def verify_payment(request: Request):
    try:
        body = await request.json()
        razorpay_order_id = body.get("razorpay_order_id")
        razorpay_payment_id = body.get("razorpay_payment_id")
        razorpay_signature = body.get("razorpay_signature")
        generated_signature = hmac.new(
            os.environ["RAZORPAY_KEY_SECRET"].encode(),
            f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
            hashlib.sha256,
        ).hexdigest()
        if generated_signature != razorpay_signature:
            return JSONResponse(
                status_code=400, content={"message": "Invalid signature"}
            )
        payment = await Payment.find_one(Payment.orderId == razorpay_order_id)
        if payment is None:
            return JSONResponse(
                status_code=404, content={"message": "Payment not found"}
            )
        payment.status = "paid"
        payment.paymentId = razorpay_payment_id
        payment.updatedAt = utc_now()
        await payment.save()
        async with httpx.AsyncClient() as http:
            await http.post(
                f"{os.environ.get('AUTH_SERVICE_URL')}/update-plan",
                json={
                    "userId": payment.userId,
                    "plan": payment.plan,
                    "credits": payment.credits,
                },
            )
        return JSONResponse(
            status_code=200, content={"message": "Payment verified successfully"}
        )
    except Exception as err:
        return JSONResponse(
            status_code=500, content={"message": f"Internal server error: {err}"}
        )
