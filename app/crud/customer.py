from sqlalchemy.orm import Session
from app.models import customer as models
from app.schemas import customer as customerSchema

def createCustomer(db: Session, customer: customerSchema.CustomerCreate):
    dbCustomer = models.Customer(**customer.model_dump())
    db.add(dbCustomer)
    db.commit()
    db.refresh(dbCustomer)
    return dbCustomer

def getCustomer(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Customer).offset(skip).limit(limit).all()