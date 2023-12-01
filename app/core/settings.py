from pydantic import BaseSettings, HttpUrl, validator


class AppSettings(BaseSettings):
    email_name: str
    email_password: str
    hostname: str
    port: int

    class Config:
        env_file = ".env"


class GoogleCredInfo(BaseSettings):
    type: str
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    auth_uri: HttpUrl
    token_uri: HttpUrl
    auth_provider_x509_cert_url: HttpUrl
    client_x509_cert_url: HttpUrl
    universe_domain: str

    @validator("private_key")
    def convert_key(cls, key: str) -> str:
        return key.replace(r"\n", "\n")

    class Config:
        env_file = ".env"


class FirebaseCredInfo(BaseSettings):
    type: str
    firebase_project_id: str
    firebase_private_key_id: str
    firebase_private_key: str
    firebase_client_email: str
    firebase_client_id: str
    auth_uri: HttpUrl
    token_uri: HttpUrl
    auth_provider_x509_cert_url: HttpUrl
    firebase_client_x509_cert_url: HttpUrl
    universe_domain: str
    firebase_database_url: HttpUrl

    @validator("firebase_private_key")
    def convert_key(cls, key: str) -> str:
        return key.replace(r"\n", "\n")

    class Config:
        env_file = ".env"


def get_app_settings():
    return AppSettings()
