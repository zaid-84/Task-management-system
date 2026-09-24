from datetime import datetime, timezone

from app.services.supabase_service import supabase


def create_task(
    title,
    description,
    created_by,
    assigned_to,
    due_date=None
):
    task_data = {
        "title": title,
        "description": description,
        "created_by": created_by,
        "assigned_to": assigned_to,
        "status": "pending",
        "due_date": due_date
    }

    response = (
        supabase
        .table("tasks")
        .insert(task_data)
        .execute()
    )

    return response.data


def get_tasks_for_user(user_id):
    response = (
        supabase
        .table("tasks")
        .select("*")
        .or_(
            f"created_by.eq.{user_id},"
            f"assigned_to.eq.{user_id}"
        )
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


def get_task_by_id(task_id):
    response = (
        supabase
        .table("tasks")
        .select("*")
        .eq("id", task_id)
        .single()
        .execute()
    )

    return response.data


def complete_task(task_id, user_id):
    # First, find the task
    response = (
        supabase
        .table("tasks")
        .select("*")
        .eq("id", task_id)
        .single()
        .execute()
    )

    task = response.data

    if not task:
        raise ValueError("Task not found")

    # Only the assigned user can complete the task
    if task["assigned_to"] != user_id:
        raise PermissionError(
            "You are not allowed to complete this task"
        )

    # Update task status
    update_response = (
        supabase
        .table("tasks")
        .update({
            "status": "completed",
            "completed_at": datetime.now(timezone.utc).isoformat()
        })
        .eq("id", task_id)
        .execute()
    )

    return update_response.data



def user_exists(user_id):
    response = (
        supabase
        .table("users")
        .select("id")
        .eq("id", user_id)
        .maybe_single()
        .execute()
    )

    return response.data is not None