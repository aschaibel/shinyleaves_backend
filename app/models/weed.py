from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Weed(Base):
    __tablename__ = "weed"

    w_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    genetic = Column(String(255))
    thc = Column(Float)
    cbd = Column(Float)
    effect = Column(String(255))
