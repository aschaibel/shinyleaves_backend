from sqlalchemy.orm import Session
from app.models import orders as models
from app.schemas import orders as ordersSchema

def createOrders(db: Session, orders: ordersSchema.OrdersCreate):
    dbOrders = models.Orders(**orders.dict())
    db.add(dbOrders)
    db.commit()
    db.refresh(dbOrders)
    return dbOrders

def getOrders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Orders).offset(skip).limit(limit).all()

