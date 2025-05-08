from pydantic import BaseModel

class CustomerBase(BaseModel):
    name: str
    address: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    c_id: int

    model_config = {
        "from_attributes": True
    }
