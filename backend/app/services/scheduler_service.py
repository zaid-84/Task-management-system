from apscheduler.schedulers.background import BackgroundScheduler

from app.services.reminder_service import check_due_date_reminders


scheduler = BackgroundScheduler()


def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            check_due_date_reminders,
            "interval",
            hours=1,
            id="due_date_reminder",
            replace_existing=True
        )

        scheduler.start()