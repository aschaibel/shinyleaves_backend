from sqlalchemy.orm import Session

from app.models import customer as models
from app.schemas import customer as customer_schemas
from app.utils.password import password_hash


def create_customer(db: Session, customer: customer_schemas.CustomerCreate):
    customer.password = password_hash(customer.password)
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customer(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Customer).offset(skip).limit(limit).all()


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.c_id == customer_id).first()
