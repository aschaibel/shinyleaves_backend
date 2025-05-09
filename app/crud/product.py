from sqlalchemy.orm import Session
from app.models import product as models
from app.schemas import product as product_schemas

# Create new Product
def create_product(db: Session, product: product_schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()