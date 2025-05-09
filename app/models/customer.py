from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import Field, EmailStr

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'

    c_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    address = Column(String(255))
    email: EmailStr = Field(unique=True)
    password = Column(String(255))



