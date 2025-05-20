from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import customer as crud
from app.schemas import customer as schemas
from app.utils.database import get_db

router = APIRouter()


@router.get("/customer/", response_model=list[schemas.Customer])
def get_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_customer(db=db, skip=skip, limit=limit)
