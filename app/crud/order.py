from sqlalchemy.orm import Session

from app.models import order as models
from app.schemas import order as order_schemas


def create_order(db: Session, order: order_schemas.OrderCreate):
    """
    Create a new order in the database.

    This function creates a new order with the provided data.

    Args:
        db (Session): Database session.
        order (order_schemas.OrderCreate): Order data to create.

    Returns:
        models.Order: The created order with its ID.
    """
    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, skip: int = 0, limit: int = 10):
    """
    Get a list of orders with pagination.

    This function retrieves a paginated list of orders from the database.

    Args:
        db (Session): Database session.
        skip (int, optional): Number of orders to skip. Defaults to 0.
        limit (int, optional): Maximum number of orders to return. Defaults to 10.

    Returns:
        list[models.Order]: List of orders.
    """
    return db.query(models.Order).offset(skip).limit(limit).all()


def get_order_by_id(db: Session, order_id: int):
    """
    Get an order by ID.

    This function retrieves a single order by its ID.

    Args:
        db (Session): Database session.
        order_id (int): ID of the order to retrieve.

    Returns:
        models.Order: The requested order, or None if not found.
    """
    return db.query(models.Order).filter(models.Order.o_id == order_id).first()
