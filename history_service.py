"""Persistence and retrieval for the unified scan history table."""
import csv
import json
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.history import ScanHistory
from app.utils.logger import get_logger

log = get_logger("history_service")


def log_scan(db: Session, *, scan_type: str, label: str, score: int,
             subject: str | None, details: dict) -> ScanHistory:
    entry = ScanHistory(
        scan_type=scan_type,
        label=label,
        score=score,
        subject=subject,
        details=json.dumps(details),
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    log.info("Logged %s scan -> %s (score=%s)", scan_type, label, score)
    return entry


def get_recent(db: Session, limit: int = 15, scan_type: str | None = None) -> list[ScanHistory]:
    q = db.query(ScanHistory)
    if scan_type:
        q = q.filter(ScanHistory.scan_type == scan_type)
    return q.order_by(ScanHistory.created_at.desc()).limit(limit).all()


def count_all(db: Session, scan_type: str | None = None) -> int:
    q = db.query(func.count(ScanHistory.id))
    if scan_type:
        q = q.filter(ScanHistory.scan_type == scan_type)
    return q.scalar() or 0


def export_csv(db: Session) -> str:
    """Write the full scan history to a timestamped CSV in reports/ and return its path."""
    rows = db.query(ScanHistory).order_by(ScanHistory.created_at.desc()).all()
    filename = f"scan_history_{datetime.utcnow():%Y%m%d_%H%M%S}.csv"
    path = settings.reports_dir / filename

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "scan_type", "label", "score", "subject", "created_at"])
        for r in rows:
            writer.writerow([r.id, r.scan_type, r.label, r.score, r.subject, r.created_at.isoformat()])

    log.info("Exported %d history rows to %s", len(rows), path)
    return str(path)
