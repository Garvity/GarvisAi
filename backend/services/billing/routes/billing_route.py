from fastapi import APIRouter

from controllers.billing_controller import create_order, verify_payment

router = APIRouter()

router.add_api_route("/create-order", create_order, methods=["POST"])
router.add_api_route("/verify-payment", verify_payment, methods=["POST"])
