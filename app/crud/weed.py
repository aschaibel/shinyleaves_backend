from sqlalchemy.orm import Session
from app.models import weed as models
from app.schemas import weed as weed_schema

def createWeed(db: Session, weed: weed_schema.WeedCreate):
    db_weed = models.Weed(**weed.dict())
    db.add(db_weed)
    db.commit()
    db.refresh(db_weed)
    return db_weed


def getWeed(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Weed).offset(skip).limit(limit).all()
