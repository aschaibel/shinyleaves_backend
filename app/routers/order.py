from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import order as crud
from app.schemas import order as schemas
from app.utils.database import get_db

router = APIRouter()


@router.post("/order/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order)


@router.get("/order/", response_model=list[schemas.Order])
def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_order(db=db, skip=skip, limit=limit)
