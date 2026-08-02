from sqlalchemy import Column, Integer

from app.core.database import Base


class Statistics(Base):
    """
    Stores dashboard statistics.
    """

    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)

    # Total scans
    total_password_checks = Column(Integer, default=0)
    total_url_scans = Column(Integer, default=0)
    total_file_scans = Column(Integer, default=0)

    # URL statistics
    safe_urls = Column(Integer, default=0)
    dangerous_urls = Column(Integer, default=0)

    # Password statistics
    weak_passwords = Column(Integer, default=0)
    medium_passwords = Column(Integer, default=0)
    strong_passwords = Column(Integer, default=0)

    # Malware statistics
    safe_files = Column(Integer, default=0)
    malicious_files = Column(Integer, default=0)