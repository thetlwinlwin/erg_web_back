from pydantic import BaseSettings, HttpUrl, validator


class AppSetting(BaseSettings):
    email_name: str
    email_password: str
    hostname: str
    port: int

    class Config:
        env_file = ".env"


class GoogleCred(BaseSettings):
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


appSetting = AppSetting()

googleCred = GoogleCred()
