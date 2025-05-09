from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import customer as crud
from app.schemas import customer as schemas
from app.models.database import get_db

router = APIRouter()

@router.post("/customer/", response_model=schemas.Customer)
def createCustomer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.createCustomer(db=db, customer=customer)

@router.get("/customer/", response_model=list[schemas.Customer])
def getCustomers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.getCustomer(db=db, skip=skip, limit=limit)