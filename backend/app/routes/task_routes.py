from flask import Blueprint, jsonify, request
from app.middleware.auth_middleware import require_auth
from datetime import datetime
from app.services.supabase_service import supabase
from app.services.notification_service import (
    send_task_assignment_email,
    send_task_completion_email
)

from app.services.task_service import (
    create_task,
    get_tasks_for_user,
    get_task_by_id,
    complete_task,
    user_exists
)



task_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/api/tasks"
)

@task_bp.route("/", methods=["POST"])
@require_auth
def create_task_route():
    
    data = request.get_json() or {}

    title = data.get("title")
    description = data.get("description")
    assigned_to = data.get("assigned_to")
    due_date = data.get("due_date")

    if not title:
        return jsonify({
            "success": False,
            "message": "title is required"
        }), 400

    if not assigned_to:
        return jsonify({
            "success": False,
            "message": "assigned_to is required"
        }), 400

    if not user_exists(assigned_to):
        return jsonify({
            "success": False,
            "message": "Assigned user does not exist"
        }), 400
    if due_date:
        try:
            datetime.fromisoformat(due_date.replace("Z", "+00:00"))
        except ValueError:
            return jsonify({
                "success": False,
                "message": "Invalid due_date format"
            }), 400

    try:
        current_user = request.current_user

        # Create task
        task = create_task(
            title=title,
            description=description,
            created_by=current_user.id,
            assigned_to=assigned_to,
            due_date=due_date
        )

        # Get assigned user's details
        user_response = (
            supabase
            .table("users")
            .select("name, email")
            .eq("id", assigned_to)
            .single()
            .execute()
        )

        assigned_user = user_response.data

        # Send notification email
        send_task_assignment_email(
            assignee_email=assigned_user["email"],
            assignee_name=assigned_user.get("name") or "User",
            task_title=title,
            task_description=description
        )

        return jsonify({
            "success": True,
            "task": task
        }), 201

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


@task_bp.route("/user/<user_id>", methods=["GET"])
@require_auth
def get_user_tasks(user_id):
    try:
        tasks = get_tasks_for_user(user_id)

        return jsonify({
            "success": True,
            "tasks": tasks
        }), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


@task_bp.route("/<task_id>", methods=["GET"])
@require_auth
def get_task(task_id):
    try:
        task = get_task_by_id(task_id)

        return jsonify({
            "success": True,
            "task": task
        }), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 404

@task_bp.route("/<task_id>/complete", methods=["PATCH"])
@require_auth
def complete_task_route(task_id):
    try:
        current_user = request.current_user

        # Get the task first
        task_response = (
            supabase
            .table("tasks")
            .select("*")
            .eq("id", task_id)
            .single()
            .execute()
        )

        task = task_response.data

        if not task:
            return jsonify({
                "success": False,
                "message": "Task not found"
            }), 404

        # Complete task
        completed_task = complete_task(
            task_id,
            current_user.id
        )

        # Get creator's information
        creator_response = (
            supabase
            .table("users")
            .select("name, email")
            .eq("id", task["created_by"])
            .single()
            .execute()
        )

        creator = creator_response.data

        # Get person who completed the task
        completed_by_response = (
            supabase
            .table("users")
            .select("name")
            .eq("id", current_user.id)
            .single()
            .execute()
        )

        completed_by = completed_by_response.data

        # Send completion notification
        send_task_completion_email(
            creator_email=creator["email"],
            creator_name=creator.get("name") or "User",
            task_title=task["title"],
            completed_by_name=completed_by.get("name") or "User"
        )

        return jsonify({
            "success": True,
            "task": completed_task
        }), 200

    except PermissionError as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 403

    except ValueError as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 404

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500
        
@task_bp.route("/", methods=["GET"])
@require_auth
def get_my_tasks():
    current_user = request.current_user

    try:
        tasks = get_tasks_for_user(current_user.id)

        return jsonify({
            "success": True,
            "tasks": tasks
        }), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500
        
