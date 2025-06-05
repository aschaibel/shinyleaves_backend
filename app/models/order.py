from sqlalchemy import Column, Integer, String, ForeignKey

from app.utils.database import Base


class Order(Base):
    __tablename__ = "order"
    o_id = Column(Integer, primary_key=True, autoincrement=True)
    p_id = Column(Integer, ForeignKey("product.p_id"), nullable=False)
    amount = Column(Integer, nullable=False)
    order_nr = Column(String, nullable=False)
