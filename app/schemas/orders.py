from pydantic import BaseModel


class OrdersBase(BaseModel):
    c_id: int
    p_id: int
    amount: float

class OrdersCreate(OrdersBase):
    pass

class Orders(OrdersBase):
    o_id: int

    model_config = {
        "from_attributes": True
    }