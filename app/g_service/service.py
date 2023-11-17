from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.core import GoogleCredInfo

from .service_type import GServiceTypes, get_scopes


class GService:
    def __init__(self, info: GoogleCredInfo):
        self._info = info

    def _build(self, service_type: GServiceTypes, version: str):
        creds: service_account.Credentials = (
            service_account.Credentials.from_service_account_info(
                info=self._info, scopes=get_scopes(service_type)
            )
        )
        return build(
            service_type.value,
            version,
            credentials=creds,
        )

    def get_drive(self, version: str = "v3"):
        return self._build(GServiceTypes.DRIVE, version)

    def get_docs(self, version: str):
        return self._build(GServiceTypes.DOCS, version)


def get_gservice():
    return GService(info=GoogleCredInfo().dict())
