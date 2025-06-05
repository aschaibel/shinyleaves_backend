from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import order as crud
from app.models.customer import Customer
from app.routers.oauth2 import get_current_user
from app.schemas import order as schemas
from app.utils.database import get_db

router = APIRouter()


@router.post("/order/", response_model=schemas.Order)
def create_order(
    order: schemas.OrderCreate, 
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user)
):
    """
    Create a new order.

    This endpoint allows creating a new order.

    Args:
        order (schemas.OrderCreate): Order data to create.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (Customer): The authenticated user.

    Returns:
        schemas.Order: The created order with its ID.
    """
    return crud.create_order(db=db, order=order)


@router.get("/orders/", response_model=list[schemas.Order])
def get_orders(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user)
):
    """
    Get a list of orders with pagination.

    This endpoint returns a paginated list of orders.

    Args:
        skip (int, optional): Number of orders to skip. Defaults to 0.
        limit (int, optional): Maximum number of orders to return. Defaults to 10.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (Customer): The authenticated user.

    Returns:
        list[schemas.Order]: List of orders.
    """
    return crud.get_order(db=db, skip=skip, limit=limit)


@router.get("/orders/{order_id}", response_model=schemas.Order)
def get_order_by_id(
    order_id: str, 
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user)
):
    """
    Get an order by ID.

    This endpoint returns a single order by its ID.

    Args:
        order_id (str): ID of the order to retrieve.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (Customer): The authenticated user.

    Returns:
        schemas.Order: The requested order.

    Raises:
        HTTPException: If the order is not found.
    """
    db_order = crud.get_order_by_id(db=db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
