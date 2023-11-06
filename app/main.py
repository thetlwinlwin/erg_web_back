from smtplib import SMTPException

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.email_sending import send_suggestion
from app.schema import Suggestion

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


@app.post("/post/email")
def posting_email(suggestion: Suggestion):
    try:
        send_suggestion(item=suggestion)
        return JSONResponse(content="success", status_code=status.HTTP_200_OK)
    except SMTPException as e:
        return JSONResponse(
            content=e, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
