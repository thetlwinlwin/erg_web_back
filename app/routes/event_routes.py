from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse, JSONResponse

from app.firebase.crud import FirebaseCrud, get_firebase_crud
from app.g_service import GoogleDrive, GServiceFactory, get_gservice

event_router = APIRouter(prefix="/events")


@event_router.get("/")
def get_events(
    firebase_crud: FirebaseCrud = Depends(get_firebase_crud),
):
    data = firebase_crud.read()
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)


@event_router.get("/refresh")
def refresh_events(
    g_service: GServiceFactory = Depends(get_gservice),
    firebase_crud: FirebaseCrud = Depends(get_firebase_crud),
):
    service = g_service.get_drive()
    data = GoogleDrive(service).refresh()
    firebase_crud.write(data)
    return JSONResponse(content="success", status_code=status.HTTP_200_OK)
