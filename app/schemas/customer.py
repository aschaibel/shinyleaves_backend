from pydantic import BaseModel, EmailStr
from typing import Optional


class TokenData(BaseModel):
    id: Optional[int] = None


class CustomerBase(BaseModel):
    name: str
    address: str
    email: str
    password: str


class CustomerCreate(CustomerBase):
    email: EmailStr
    password: str
    pass


class Customer(CustomerBase):
    c_id: int

    model_config = {"from_attributes": True}


class CustomerLogin(BaseModel):
    email: EmailStr
    password: str
