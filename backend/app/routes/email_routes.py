from flask import Blueprint, jsonify

from app.services.email_service import send_email


email_bp = Blueprint(
    "email",
    __name__,
    url_prefix="/api/email"
)

