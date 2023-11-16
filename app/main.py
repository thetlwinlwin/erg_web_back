from smtplib import SMTPException

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.mail_handler.email_sending import send_suggestion
from app.routes import email_router
from app.schemas.suggestion_schema import Suggestion

app = FastAPI(
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://ever-rich-group-web.web.app"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(email_router)
