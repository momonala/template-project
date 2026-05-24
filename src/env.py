"""Secrets loaded from .env (copy .env.example to .env for local development)."""

import os
from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "")
TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN", "")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "")
