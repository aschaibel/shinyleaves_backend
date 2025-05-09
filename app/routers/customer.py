from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import customer as crud
from app.schemas import customer as schemas
from app.models.database import get_db

router = APIRouter()

@router.post("/customer/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db=db, customer=customer)

@router.get("/customer/", response_model=list[schemas.Customer])
def get_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_customer(db=db, skip=skip, limit=limit)