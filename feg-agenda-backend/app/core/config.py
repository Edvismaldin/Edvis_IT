from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List, Optional
import secrets
import os


class Settings(BaseSettings):
    project_name: str = "FEG Agenda API"

    # Database
    sqlite_db_path: str = os.getenv("SQLITE_DB_PATH", "/workspace/feg-agenda-backend/data/app.db")

    # Security / Auth
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 8 * 60  # 8 hours

    # Admin seeding
    admin_email: str = os.getenv("ADMIN_EMAIL", "admin@feg.br")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "admin123")

    # CORS
    backend_cors_origins: List[AnyHttpUrl] | List[str] = ["*"]


settings = Settings()  # type: ignore[call-arg]