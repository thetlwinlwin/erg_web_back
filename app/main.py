from smtplib import SMTPException
from fastapi import FastAPI,status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.schema import Suggestion
from app.email_sending import send_suggestion


app = FastAPI()

app.add_middleware(CORSMiddleware,allow_origins=["*"],)

@app.post('/post/email')
async def posting_email(suggestion: Suggestion):
    try:
        res = send_suggestion(item= suggestion)
        return JSONResponse(content='success',status_code=status.HTTP_200_OK)
    except SMTPException as e:
        return JSONResponse(content=e,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

