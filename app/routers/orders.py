from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import orders as crud
from app.schemas import orders as schemas
from app.models.database import get_db

router = APIRouter()

@router.post("/orders/", response_model=schemas.Orders)
def createOrders(orders: schemas.OrdersCreate, db: Session = Depends(get_db)):
    return crud.createOrders(db=db, orders=orders)

@router.get("/orders/", response_model=list[schemas.Orders])
def getOrders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.getOrders(db=db, skip=skip, limit=limit)