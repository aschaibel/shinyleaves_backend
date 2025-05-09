from sqlalchemy.orm import Session
from app.models import orders as models
from app.schemas import orders as orders_schemas

def create_orders(db: Session, orders: orders_schemas.OrdersCreate):
    db_orders = models.Orders(**orders.dict())
    db.add(db_orders)
    db.commit()
    db.refresh(db_orders)
    return db_orders

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Orders).offset(skip).limit(limit).all()

