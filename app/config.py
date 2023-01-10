from pydantic import BaseSettings

class AppSetting(BaseSettings):
    email_name: str
    email_password:str
    hostname :str
    port :int
    
    class Config:
        env_file = '.env'


appSetting = AppSetting()