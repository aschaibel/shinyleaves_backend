from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: float
    w_id: int
    slug: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    slug: Optional[str]


class Product(ProductBase):
    p_id: int

    model_config = {"from_attributes": True}
