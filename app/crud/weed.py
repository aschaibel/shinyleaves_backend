from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import weed as models
from app.schemas import weed as weed_schemas


def create_weed(db: Session, weed: list[weed_schemas.WeedCreate]):
    try:
        db_weed = [models.Weed(**w.model_dump()) for w in weed]
        db.add_all(db_weed)
        db.commit()
        for db_w in db_weed:
            db.refresh(db_w)
        return db_weed
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Integrity error occurred: {str(e.orig)}")
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error occurred: {str(e)}")
    except Exception as e:
        db.rollback()
        raise Exception(f"An unexpected error occurred: {str(e)}")


def get_weed(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Weed).offset(skip).limit(limit).all()


def get_weed_by_id(db: Session, weed_id: int):
    try:
        if not isinstance(weed_id, int):
            raise ValueError("weed_id must be an integer")
        weed = db.query(models.Weed).filter(models.Weed.w_id == weed_id).first()
        if weed is None:
            raise ValueError(f"Weed with id {weed_id} does not exist")
        return weed
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to get weed by id: {str(e)}")


def delete_weed(db: Session, weed_id: int):
    weed_to_delete = db.query(models.Weed).filter(models.Weed.w_id == weed_id).first()

    if not weed_to_delete:
        raise HTTPException(status_code=404, detail="Weed not found")

    try:
        db.delete(weed_to_delete)
        db.commit()
        return {"status_code": 204, "detail": "Weed deleted successfully"}

    except IntegrityError as error:
        db.rollback()

        # Check if the error is a foreign key constraint violation (MySQL error code 1451)
        if hasattr(error.orig, "args") and error.orig.args[0] == 1451:
            raise HTTPException(
                status_code=422,
                detail="Cannot delete weed: it is still referenced by one or more products.",
            )

        # Otherwise, re-raise the raw error
        raise HTTPException(
            status_code=500, detail=f"Integrity error during deletion: {str(error)}"
        )

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database error during deletion: {str(error)}"
        )

    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Unknown error during deletion: {str(error)}"
        )
