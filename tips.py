from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class SecurityTip(Base):
    """
    Stores cybersecurity tips displayed on the dashboard.
    """

    __tablename__ = "security_tips"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String(100),
        nullable=False
    )

    tip = Column(
        Text,
        nullable=False
    )

    category = Column(
        String(50),
        nullable=False
    )