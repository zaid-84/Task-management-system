import os

from dotenv import load_dotenv


load_dotenv()

class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False")

    FRONTEND_URL = os.getenv(
        "FRONTEND_URL",
        "http://localhost:3000"
    )

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
    GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
    GMAIL_REFRESH_TOKEN = os.getenv("GMAIL_REFRESH_TOKEN")