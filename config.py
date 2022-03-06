from pydantic import BaseModel
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class AppConfig(BaseModel):
    jwt_secret: str = getenv('JWT_SECRET')

app_config = AppConfig()