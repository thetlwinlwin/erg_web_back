import smtplib as smt
from email.message import EmailMessage

from app.core import appSetting
from app.schemas.suggestion_schema import Suggestion


def send_suggestion(item: Suggestion):
    incoming_msg = EmailMessage()
    incoming_msg["Subject"] = f"New Suggestion"
    incoming_msg.set_content(item.suggestion)
    mail = smt.SMTP(host=appSetting.hostname, port=appSetting.port)
    mail.starttls()
    mail.login(user=appSetting.email_name, password=appSetting.email_password)
    mail.send_message(
        msg=incoming_msg,
        from_addr=appSetting.email_name,
        to_addrs=appSetting.email_name,
    )
    mail.quit()
