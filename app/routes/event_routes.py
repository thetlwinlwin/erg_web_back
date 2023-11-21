from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse, JSONResponse

from app.g_service import FieldNames, GoogleDrive, GServiceFactory, get_gservice

event_router = APIRouter(prefix="/events")


@event_router.get("/")
def get_events():
    return FileResponse("events.json")


@event_router.get("/refresh")
def update_text(
    g_service: GServiceFactory = Depends(get_gservice),
):
    service = g_service.get_drive()
    GoogleDrive(service).refresh()
    return JSONResponse(content="success", status_code=status.HTTP_200_OK)


@event_router.get("/refresh/{field_name}")
def refresh_events(
    field_name: FieldNames,
    g_service: GServiceFactory = Depends(get_gservice),
):
    service = g_service.get_drive()
    GoogleDrive(service=service).update(field=field_name)
    return JSONResponse(content="success", status_code=status.HTTP_200_OK)
