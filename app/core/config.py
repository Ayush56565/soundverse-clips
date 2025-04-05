from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Clips Service"
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"{self.DATABASE_URL}"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()