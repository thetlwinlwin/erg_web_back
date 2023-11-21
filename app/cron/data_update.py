from app.g_service import GoogleDrive, get_gservice


def cron():
    service = get_gservice().get_drive()
    GoogleDrive(service).refresh()
