from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import product as crud
from app.schemas import product as schemas
from app.models.database import get_db

router = APIRouter()

@router.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@router.get("/products/", response_model=list[schemas.Product])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_products(db=db, skip=skip, limit=limit)