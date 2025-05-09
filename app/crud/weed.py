from sqlalchemy.orm import Session
from app.models import weed as models
from app.schemas import weed as weed_schemas

def create_weed(db: Session, weed: weed_schemas.WeedCreate):
    db_weed = models.Weed(**weed.dict())
    db.add(db_weed)
    db.commit()
    db.refresh(db_weed)
    return db_weed


def get_weed(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Weed).offset(skip).limit(limit).all()
