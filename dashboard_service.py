"""Aggregates ScanHistory rows into the shapes the dashboard's Chart.js views need."""
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.history import ScanHistory
from app.models.statistics import KnownThreatHash


def _counts_by_label(db: Session, scan_type: str) -> dict[str, int]:
    rows = (
        db.query(ScanHistory.label, func.count(ScanHistory.id))
        .filter(ScanHistory.scan_type == scan_type)
        .group_by(ScanHistory.label)
        .all()
    )
    return {label: count for label, count in rows}


def get_dashboard_stats(db: Session, recent_limit: int = 15) -> dict:
    passwords_by_strength = _counts_by_label(db, "password")
    urls_by_verdict = _counts_by_label(db, "url")
    files_by_verdict = _counts_by_label(db, "file")

    totals = {
        "passwords_checked": sum(passwords_by_strength.values()),
        "urls_scanned": sum(urls_by_verdict.values()),
        "files_scanned": sum(files_by_verdict.values()),
    }

    threat_intel_size = db.query(func.count(KnownThreatHash.sha256)).scalar() or 0

    recent = (
        db.query(ScanHistory)
        .order_by(ScanHistory.created_at.desc())
        .limit(recent_limit)
        .all()
    )
    recent_activity = [
        {"type": r.scan_type, "label": r.label, "created_at": r.created_at.isoformat()}
        for r in recent
    ]

    return {
        "totals": totals,
        "passwords_by_strength": passwords_by_strength,
        "urls_by_verdict": urls_by_verdict,
        "files_by_verdict": files_by_verdict,
        "threat_intel_size": threat_intel_size,
        "recent_activity": recent_activity,
    }
