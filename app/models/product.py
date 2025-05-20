from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Float, ForeignKey

from app.utils.database import Base


class Product(Base):
    __tablename__ = "product"
    p_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    w_id = Column(Integer, ForeignKey("weed.w_id"), nullable=False)
    slug = Column(String(255), nullable=True)


class ProductBase(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=255, description="Name cannot be empty"
    )
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    w_id: int
    slug: str = Field(None, description="Path to the product picture")
