from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.crud import product as crud
from app.crud.product import delete_product_by_id
from app.schemas import product as schemas
from app.utils.database import get_db

router = APIRouter()


@router.post("/products/", response_model=List[schemas.Product])
def create_products(
    product: List[schemas.ProductCreate], db: Session = Depends(get_db)
):
    return [crud.create_product(db=db, product=p) for p in product]


@router.get("/products/", response_model=list[schemas.Product])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_products(db=db, skip=skip, limit=limit)


@router.patch("/products/{product_id}", response_model=schemas.Product)
def patch_product(
    product_id: int, update_data: schemas.ProductUpdate, db: Session = Depends(get_db)
):
    product = crud.update_products(db, product_id, update_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/products/{product_id}")
async def remove_product_by_id(product_id: int, db: Session = Depends(get_db)):
    delete_product_by_id(db, product_id)
    return Response(status_code=204)
