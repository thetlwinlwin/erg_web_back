from fastapi import APIRouter, Depends, status

from app.g_service import GService, get_gservice

event_router = APIRouter(prefix="/events")


@event_router.get("/")
def get_events(g_service: GService = Depends(get_gservice)):
    service = g_service.get_drive()
    results = service.files().list().execute()
    # get the results
    items = results.get("files", [])
    print(items)
