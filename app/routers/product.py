from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import product as crud
from app.schemas import product as schemas
from app.models.database import get_db

router = APIRouter()

@router.post("/products/", response_model=schemas.Product)
def createProduct(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.createProduct(db=db, product=product)

@router.get("/products/", response_model=list[schemas.Product])
def getProducts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.getProduct(db=db, skip=skip, limit=limit)