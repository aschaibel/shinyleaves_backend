from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import customer as crud
from app.schemas import customer as schemas
from app.utils.database import get_db

router = APIRouter()


@router.get("/customer/", response_model=list[schemas.Customer])
def get_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get a list of customers with pagination.

    This endpoint returns a paginated list of customers.

    Args:
        skip (int, optional): Number of customers to skip. Defaults to 0.
        limit (int, optional): Maximum number of customers to return. Defaults to 10.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        list[schemas.Customer]: List of customers.
    """
    return crud.get_customer(db=db, skip=skip, limit=limit)


@router.get("/customer/{customer_id}", response_model=schemas.Customer)
def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    """
    Get a customer by ID.

    This endpoint returns a single customer by its ID.

    Args:
        customer_id (int): ID of the customer to retrieve.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        schemas.Customer: The requested customer.

    Raises:
        HTTPException: If the customer is not found.
    """
    db_customer = crud.get_customer_by_id(db=db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer
