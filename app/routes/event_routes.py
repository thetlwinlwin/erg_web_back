from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.g_service import GService, get_gservice
from app.g_service.gdrive import GoogleDrive

event_router = APIRouter(prefix="/events")


@event_router.get("/update")
def get_events(
    g_service: GService = Depends(get_gservice),
):
    service = g_service.get_drive()
    GoogleDrive(service).update_docs()
    return JSONResponse(content="success", status_code=status.HTTP_200_OK)


@event_router.get("/refresh")
def refresh_events(
    g_service: GService = Depends(get_gservice),
):
    service = g_service.get_drive()
    GoogleDrive(service=service).refresh()
    return JSONResponse(content="success", status_code=status.HTTP_200_OK)
