from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import email_router

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
