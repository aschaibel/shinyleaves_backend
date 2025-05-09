from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import weed as crud
from app.schemas import weed as schemas
from app.models.database import get_db

router = APIRouter()

@router.post("/weed/", response_model=schemas.Weed)
def createWeed(weed: schemas.WeedCreate, db: Session = Depends(get_db)):
    return crud.createWeed(db=db, weed=weed)

@router.get("/weed/", response_model=list[schemas.Weed])
def getWeed(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.getWeed(db=db, skip=skip, limit=limit)
