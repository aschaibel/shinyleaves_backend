from sqlalchemy.orm import Session

from app.models import order as models
from app.schemas import order as order_schemas


def create_order(db: Session, order: order_schemas.OrderCreate):
    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Order).offset(skip).limit(limit).all()
