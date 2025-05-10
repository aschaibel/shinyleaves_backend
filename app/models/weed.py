from sqlalchemy import Column, Integer, String, Float

from app.utils.database import Base


class Weed(Base):
    __tablename__ = "weed"
    w_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    genetic = Column(String(255), nullable=False)
    thc = Column(Float, nullable=False)
    cbd = Column(Float, nullable=False)
    effect = Column(String(255), nullable=False)
