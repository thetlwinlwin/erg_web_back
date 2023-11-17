import smtplib as smt
from email.message import EmailMessage

from app.core import AppSettings
from app.schemas.suggestion_schema import Suggestion


def send_suggestion(item: Suggestion, settings: AppSettings):
    incoming_msg = EmailMessage()
    incoming_msg["Subject"] = f"New Suggestion"
    incoming_msg.set_content(item.suggestion)
    mail = smt.SMTP(host=settings.hostname, port=settings.port)
    mail.starttls()
    mail.login(user=settings.email_name, password=settings.email_password)
    mail.send_message(
        msg=incoming_msg,
        from_addr=settings.email_name,
        to_addrs=settings.email_name,
    )
    mail.quit()
