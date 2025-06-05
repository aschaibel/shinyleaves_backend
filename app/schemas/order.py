from pydantic import BaseModel


class OrderBase(BaseModel):
    c_id: int
    p_id: int
    amount: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    o_id: str

    model_config = {
        "from_attributes": True
    }
