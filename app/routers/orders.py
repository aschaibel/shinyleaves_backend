from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import orders as crud
from app.schemas import orders as schemas
from app.models.database import get_db

router = APIRouter()

@router.post("/orders/", response_model=schemas.Orders)
def create_orders(orders: schemas.OrdersCreate, db: Session = Depends(get_db)):
    return crud.create_orders(db=db, orders=orders)

@router.get("/orders/", response_model=list[schemas.Orders])
def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_orders(db=db, skip=skip, limit=limit)