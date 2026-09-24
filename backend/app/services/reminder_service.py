from datetime import datetime, timezone, timedelta

from app.services.supabase_service import supabase
from app.services.notification_service import send_task_reminder_email


def check_due_date_reminders():
    now = datetime.now(timezone.utc)
    reminder_limit = now + timedelta(hours=24)

    response = (
        supabase
        .table("tasks")
        .select("*")
        .eq("status", "pending")
        .eq("reminder_sent", False)
        .not_.is_("due_date", "null")
        .execute()
    )

    tasks = response.data or []

    for task in tasks:
        due_date = datetime.fromisoformat(
            task["due_date"].replace("Z", "+00:00")
        )

        # Send reminder if task is due within next 24 hours
        if now <= due_date <= reminder_limit:

            user_response = (
                supabase
                .table("users")
                .select("name, email")
                .eq("id", task["assigned_to"])
                .single()
                .execute()
            )

            user = user_response.data

            if not user:
                continue

            send_task_reminder_email(
                assignee_email=user["email"],
                assignee_name=user.get("name") or "User",
                task_title=task["title"],
                due_date=task["due_date"]
            )

            # Mark reminder as sent
            (
                supabase
                .table("tasks")
                .update({
                    "reminder_sent": True
                })
                .eq("id", task["id"])
                .execute()
            )