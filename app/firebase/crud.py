import firebase_admin
from fastapi import HTTPException, status
from firebase_admin import credentials, db

from app.core.settings import FirebaseCredInfo


class FirebaseCrud:
    def __init__(self, creds: FirebaseCredInfo) -> None:
        self._certificate = credentials.Certificate(
            {
                "type": creds.type,
                "project_id": creds.firebase_project_id,
                "private_key_id": creds.firebase_private_key_id,
                "private_key": creds.firebase_private_key,
                "client_email": creds.firebase_client_email,
                "client_id": creds.firebase_client_id,
                "auth_uri": creds.auth_uri,
                "token_uri": creds.token_uri,
                "auth_provider_x509_cert_url": creds.auth_provider_x509_cert_url,
                "client_x509_cert_url": creds.firebase_client_x509_cert_url,
                "universe_domain": creds.universe_domain,
            }
        )
        if not firebase_admin._apps:
            firebase_admin.initialize_app(
                self._certificate,
                {"databaseURL": creds.firebase_database_url},
            )
        self._db = db.reference()

    def write(self, data: dict) -> None:
        try:
            self._db.set(data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Contact to the admin",
            )

    def read(self) -> dict:
        return self._db.get()


def get_firebase_crud() -> FirebaseCrud:
    return FirebaseCrud(creds=FirebaseCredInfo())
