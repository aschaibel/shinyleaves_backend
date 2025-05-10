from sqlalchemy import Column, Integer, Float, ForeignKey

from app.models.database import Base


class Orders(Base):
    __tablename__ = "orders"
    o_id = Column(Integer, primary_key=True, autoincrement=True)
    c_id = Column(Integer, ForeignKey("customer.c_id"), nullable=False)
    amount = Column(Float, nullable=False)
