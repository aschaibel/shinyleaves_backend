from sqlalchemy import Column, Integer, String

from app.utils.database import Base


class Customer(Base):
    __tablename__ = "customer"

    c_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
