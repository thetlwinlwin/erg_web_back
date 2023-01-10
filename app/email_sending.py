from email.message import EmailMessage
from app.config import appSetting
import smtplib as smt

from app.schema import Suggestion



def send_suggestion(item:Suggestion):
    incoming_msg = EmailMessage()
    incoming_msg['Subject']= f'Suggestion from {item.name}'
    incoming_msg.set_content(item.suggestion)
    mail = smt.SMTP(host=appSetting.hostname,port=appSetting.port)
    mail.starttls()
    mail.login(user=appSetting.email_name, password= appSetting.email_password) 
    mail.send_message(msg=incoming_msg,from_addr=appSetting.email_name,to_addrs=appSetting.email_name)
    mail.quit()

 

    