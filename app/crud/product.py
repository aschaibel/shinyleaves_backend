from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import product as models
from app.schemas import product as product_schemas


# Create a new Product
def create_product(db: Session, product: product_schemas.ProductCreate):
    if not product.name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if product.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than zero")

    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Get all products
def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()


# Update an existing product
def update_products(db: Session, p_id: int, update_data: product_schemas.ProductUpdate):
    try:
        product = db.query(models.Product).filter(models.Product.p_id == p_id).first()
        if not product:
            return None

        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise Exception(f"Error updating product: {str(e)}")


def delete_product_by_id(db: Session, p_id: int):
    product_to_delete = (
        db.query(models.Product).filter(models.Product.p_id == p_id).first()
    )

    if not product_to_delete:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        db.delete(product_to_delete)
        db.commit()
        return {"status_code": 204, "detail": "Product deleted successfully"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database error during deletion: {str(e)}"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Unknown error during deletion: {str(e)}"
        )
