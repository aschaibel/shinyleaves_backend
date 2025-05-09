from sqlalchemy.orm import Session
from app.models import product as models
from app.schemas import product as productSchema

def createProduct(db: Session, product: productSchema.ProductCreate):
    dbProduct = models.Product(**product.model_dump())
    db.add(dbProduct)
    db.commit()
    db.refresh(dbProduct)
    return dbProduct

def getProduct(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()