from functools import wraps

from flask import request, jsonify
from supabase import create_client

from app.config import Config


supabase_auth = create_client(
    Config.SUPABASE_URL,
    Config.SUPABASE_KEY
)


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "success": False,
                "message": "Authorization header is required"
            }), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({
                "success": False,
                "message": "Invalid authorization format"
            }), 401

        token = auth_header.split(" ", 1)[1]

        try:
            response = supabase_auth.auth.get_user(token)

            if not response or not response.user:
                return jsonify({
                    "success": False,
                    "message": "Invalid or expired token"
                }), 401

            request.current_user = response.user

        except Exception:
            return jsonify({
                "success": False,
                "message": "Authentication failed"
            }), 401

        return f(*args, **kwargs)

    return decorated