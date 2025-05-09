from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import weed as crud
from app.schemas import weed as schemas
from app.models.database import get_db

router = APIRouter()

@router.post("/weed/", response_model=schemas.Weed)
def create_weed(weed: schemas.WeedCreate, db: Session = Depends(get_db)):
    return crud.create_weed(db=db, weed=weed)

@router.get("/weed/", response_model=list[schemas.Weed])
def get_weed(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_weed(db=db, skip=skip, limit=limit)
