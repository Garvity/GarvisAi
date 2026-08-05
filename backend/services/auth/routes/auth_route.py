from fastapi import APIRouter

from controllers.auth_controller import (
    deduct_credits,
    log_out,
    login,
    update_user_payment_status,
)

router = APIRouter()

router.add_api_route("/login", login, methods=["POST"])
router.add_api_route("/logout", log_out, methods=["GET"])
router.add_api_route("/update-plan", update_user_payment_status, methods=["POST"])
router.add_api_route("/deduct-credits", deduct_credits, methods=["POST"])
