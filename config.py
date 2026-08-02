import os
from pathlib import Path

from dotenv import load_dotenv

# -----------------------------
# Base Directory
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")


class Settings:
    """
    Application configuration settings.
    """

    # -----------------------------
    # Project Information
    # -----------------------------
    PROJECT_NAME = "CyberShield"
    PROJECT_VERSION = "1.0.0"
    PROJECT_DESCRIPTION = "Cyber Security Dashboard Backend"

    # -----------------------------
    # API Configuration
    # -----------------------------
    API_PREFIX = "/api"

    # -----------------------------
    # Database
    # -----------------------------
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR}/database/cybershield.db"
    )

    # -----------------------------
    # Upload Folder
    # -----------------------------
    UPLOAD_FOLDER = BASE_DIR / "uploads"

    # -----------------------------
    # Reports Folder
    # -----------------------------
    REPORT_FOLDER = BASE_DIR / "reports"

    # -----------------------------
    # Security
    # -----------------------------
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key"
    )

    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    # -----------------------------
    # VirusTotal API
    # -----------------------------
    VIRUSTOTAL_API_KEY = os.getenv(
        "VIRUSTOTAL_API_KEY",
        ""
    )

    # -----------------------------
    # Allowed File Extensions
    # -----------------------------
    ALLOWED_EXTENSIONS = {
        ".exe",
        ".dll",
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".zip",
        ".rar",
        ".7z",
        ".txt"
    }

    # -----------------------------
    # Maximum Upload Size
    # -----------------------------
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB


settings = Settings()