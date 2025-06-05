from pydantic import BaseModel


class OrderBase(BaseModel):
    p_id: int
    amount: int

class OrderCreate(OrderBase):
    order_nr: str

class Order(OrderBase):
    o_id: int
    order_nr: str

    model_config = {
        "from_attributes": True
    }
