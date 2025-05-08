from pydantic import BaseModel

class WeedBase(BaseModel):
    genetic: str
    thc: str
    cbd: str
    effect: str


class WeedCreate(WeedBase):
    pass

class Weed(WeedBase):
    w_id: int

    model_config = {
        "from_attributes": True
    }