import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env.dev"
load_dotenv(ENV_FILE_PATH)

SECRET_KEY = os.environ.get("SECRET_KEY", "YOUR-FALLBACK-SECRET-KEY")
DATABASE_URI = "sqlite:///database.db"


class DevConfig:
    TESTING = True
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    STATIC_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
