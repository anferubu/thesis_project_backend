"""
Defines the functionality for sending emails using FastAPI-Mail.

It includes:
  - send_email(): Send an email to one or multiple recipients.

"""

from pathlib import Path
from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import EmailStr

from core.secrets import env



EMAIL_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates/email"



EMAIL_CONFIG = ConnectionConfig(
    MAIL_USERNAME=env.mail_username,
    MAIL_PASSWORD=env.mail_password,
    MAIL_FROM=env.mail_from,
    MAIL_FROM_NAME=env.mail_from_name,
    MAIL_PORT=env.mail_port,
    MAIL_SERVER=env.mail_server,
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=EMAIL_TEMPLATE_DIR,
)


fm = FastMail(EMAIL_CONFIG)



async def send_email(
    to: List[EmailStr],
    subject: str,
    body: str = None,
    template_name: str = None,
    template_context: dict = None
):
    """
    Sends an email.

    Args:
      - to (List[EmailStr]): List of recipient email addresses.
      - subject (str): Email subject.
      - body (str): Email body.
      - template_name (str, optional): Name of the email template
          (default: None).
      - template_context (dict, optional): Context data for the email template
          (default: None).
    """

    message = MessageSchema(
        subject=subject,
        recipients=to,
        body=body,
        subtype="html"
    )

    if template_name:
        template_context = template_context or {}
        message.template_body = template_context

    await fm.send_message(
        message,
        template_name=template_name if template_name else None
    )
