from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HistoryResponse(BaseModel):
    """
    Response schema for a scan history record.
    """

    id: int
    scan_type: str
    target: str
    status: str
    risk_score: int
    details: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True