from sqlalchemy import Column, Integer, String, ForeignKey

from app.utils.database import Base


class Order(Base):
    __tablename__ = "order"
    o_id = Column(String, primary_key=True)
    c_id = Column(Integer, ForeignKey("customer.c_id"), nullable=False)
    p_id = Column(Integer, ForeignKey("product.p_id"), nullable=False)
    amount = Column(Integer, nullable=False)
