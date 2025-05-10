from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: float
    w_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]


class Product(ProductBase):
    p_id: int

    model_config = {"from_attributes": True}
