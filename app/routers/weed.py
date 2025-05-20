from typing import Union, List

from fastapi import APIRouter, Depends, HTTPException, status, Body, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from app.crud import weed as crud
from app.crud.weed import delete_weed
from app.schemas import weed as schemas
from app.utils.database import get_db

router = APIRouter()


@router.post("/weed/", response_model=List[schemas.Weed])
def create_weed(
    weed_input: Union[schemas.WeedCreate, List[schemas.WeedCreate]] = Body(...),
    db: Session = Depends(get_db),
):
    try:
        # Normalize to list
        weed_list = weed_input if isinstance(weed_input, list) else [weed_input]
        create_w = crud.create_weed(db=db, weed=weed_list)
        return create_w
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Integrity error: {str(e.orig)}",
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while creating weed.",
        )


@router.get("/weed/", response_model=list[schemas.Weed])
def get_weed(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        return crud.get_weed(db=db, skip=skip, limit=limit)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while getting weed.",
        )


@router.get("/weed/{weed_id}", response_model=schemas.Weed)
def get_weed_by_id(weed_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_weed_by_id(db=db, weed_id=weed_id)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while getting weed id.",
        )


@router.delete("/weed/{weed_id}")
async def remove_weed_by_id(weed_id: int, db: Session = Depends(get_db)):
    delete_weed(db, weed_id)
    return Response(status_code=204)
