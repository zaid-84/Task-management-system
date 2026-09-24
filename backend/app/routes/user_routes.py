from flask import Blueprint, jsonify, request

from app.middleware.auth_middleware import require_auth
from app.services.user_service import sync_user
from app.services.supabase_service import supabase


user_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/api/users"
)


@user_bp.route("/", methods=["GET"])
@require_auth
def get_users():
    try:
        current_user = request.current_user

        response = (
            supabase
            .table("users")
            .select("id, name, email, avatar_url")
            .neq("id", current_user.id)
            .order("name")
            .execute()
        )

        return jsonify({
            "success": True,
            "users": response.data
        }), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


@user_bp.route("/sync", methods=["POST"])
@require_auth
def sync_current_user():
    try:
        user = request.current_user

        user_data = sync_user(user)

        return jsonify({
            "success": True,
            "user": user_data
        }), 200
    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500
        
