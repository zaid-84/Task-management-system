from app.services.email_service import send_email


def send_task_assignment_email(
    assignee_email,
    assignee_name,
    task_title,
    task_description
):
    subject = f"New Task Assigned: {task_title}"

    body = f"""
Hello {assignee_name},

You have been assigned a new task.

Task:
{task_title}

Description:
{task_description or "No description provided."}

Please log in to the Task Management System to view and complete the task.

Regards,
Task Management System
"""

    return send_email(
        assignee_email,
        subject,
        body
    )
    
def send_task_completion_email(
    creator_email,
    creator_name,
    task_title,
    completed_by_name
):
    subject = f"Task Completed: {task_title}"

    body = f"""
Hello {creator_name},

Your task has been completed.

Task:
{task_title}

Completed by:
{completed_by_name}

The task has been marked as completed in the Task Management System.

Regards,
Task Management System
"""

    return send_email(
        creator_email,
        subject,
        body
    )
    
def send_task_reminder_email(
    assignee_email,
    assignee_name,
    task_title,
    due_date
):
    subject = f"Task Reminder: {task_title}"

    body = f"""
Hello {assignee_name},

This is a reminder that your task is due within the next 24 hours.

Task:
{task_title}

Due date:
{due_date}

Please complete the task before the deadline.

Regards,
Task Management System
"""

    return send_email(
        assignee_email,
        subject,
        body
    )