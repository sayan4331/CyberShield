from sqlalchemy.orm import Session

from app.models.tips import Tip


def list_tips(db: Session) -> list[Tip]:
    return db.query(Tip).order_by(Tip.category, Tip.id).all()
