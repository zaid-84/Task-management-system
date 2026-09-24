import os
import base64

from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]


def get_gmail_service():
    credentials = Credentials(
        token=None,
        refresh_token=os.getenv("GMAIL_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GMAIL_CLIENT_ID"),
        client_secret=os.getenv("GMAIL_CLIENT_SECRET"),
        scopes=SCOPES
    )

    credentials.refresh(Request())

    return build(
        "gmail",
        "v1",
        credentials=credentials
    )


def send_email(to_email, subject, body):
    service = get_gmail_service()

    message = MIMEText(body)

    message["to"] = to_email
    message["subject"] = subject

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    result = service.users().messages().send(
        userId="me",
        body={
            "raw": encoded_message
        }
    ).execute()

    return result