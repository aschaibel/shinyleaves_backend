from sqlalchemy import Column, Integer, Float, ForeignKey

from app.utils.database import Base


class Order(Base):
    __tablename__ = "order"
    o_id = Column(Integer, primary_key=True, autoincrement=True)
    c_id = Column(Integer, ForeignKey("customer.c_id"), nullable=False)
    p_id = Column(Integer, ForeignKey("product.p_id"), nullable=False)
    amount = Column(Float, nullable=False)
