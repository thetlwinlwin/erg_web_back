from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.core import GoogleCredInfo

from .service_type import GServiceTypes, get_scopes


class GService:
    def __init__(self, info: GoogleCredInfo):
        self._info = info

    def build(self, service_type: GServiceTypes, version: str):
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


class GServiceFactory:
    def __init__(
        self,
        info: GoogleCredInfo,
    ) -> None:
        self._info = info

    def get_docs(
        self,
        version: str = "v1",
    ):
        return GService(
            info=self._info,
        ).build(
            service_type=GServiceTypes.DOCS,
            version=version,
        )

    def get_drive(
        self,
        version: str = "v3",
    ):
        return GService(
            info=self._info,
        ).build(
            service_type=GServiceTypes.DRIVE,
            version=version,
        )


def get_gservice():
    return GServiceFactory(info=GoogleCredInfo().dict())
