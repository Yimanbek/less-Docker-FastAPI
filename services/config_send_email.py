import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USER: str = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD: str = os.getenv('EMAIL_PASSWORD')

settings = Settings()