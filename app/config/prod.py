import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"
load_dotenv(ENV_FILE_PATH)

SECRET_KEY = os.environ.get("SECRET_KEY", "YOUR-FALLBACK-SECRET-KEY")
DATABASE_URI = "sqlite:///database.db"


class ProdConfig:
    TESTING = False
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False
    STATIC_AUTO_RELOAD = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "YOUR-FALLBACK-SECRET-KEY")
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
