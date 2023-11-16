from smtplib import SMTPException

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.mail_handler.email_sending import send_suggestion
from app.schemas.suggestion_schema import Suggestion

email_router = APIRouter(prefix="email")


@email_router.post("/")
def send_email(suggestion: Suggestion):
    try:
        send_suggestion(item=suggestion)
        return JSONResponse(content="success", status_code=status.HTTP_200_OK)
    except SMTPException as e:
        return JSONResponse(
            content=e, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
