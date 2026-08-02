from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import rate_limit
from app.schemas.url import UrlScanRequest, UrlScanResponse
from app.services import url_service

router = APIRouter(prefix="/api/url", tags=["URL Scanner"])


@router.post("/scan", response_model=UrlScanResponse, dependencies=[Depends(rate_limit)])
def scan_url(body: UrlScanRequest, db: Session = Depends(get_db)):
    if not body.url.strip():
        raise HTTPException(400, "URL is required")
    return url_service.scan_and_log(db, body.url)
