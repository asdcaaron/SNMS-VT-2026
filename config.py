"""Application configuration loaded from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "snms-vt-development-key-change-before-deployment"
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'monitoring.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONITOR_INTERVAL_SECONDS = int(os.environ.get("MONITOR_INTERVAL_SECONDS", "60"))
    PING_TIMEOUT_SECONDS = float(os.environ.get("PING_TIMEOUT_SECONDS", "2"))
