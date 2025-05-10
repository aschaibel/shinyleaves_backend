from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import customer as crud
from app.models import customer as models
from app.schemas import customer as schemas
from app.utils.database import get_db
from app.utils.password import password_hash

router = APIRouter()


@router.post("/customer/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    # Check for existing email
    existing = (
        db.query(models.Customer)
        .filter(models.Customer.email == customer.email)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = password_hash(customer.password)
    customer.password = hashed_password
    new_customer = models.Customer(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

    # return crud.create_customer(db=db, customer=customer)


@router.get("/customer/", response_model=list[schemas.Customer])
def get_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_customer(db=db, skip=skip, limit=limit)
