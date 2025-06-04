from sqlalchemy.orm import Session

from app.models import customer as models
from app.schemas import customer as customer_schemas
from app.utils.password import password_hash


def create_customer(db: Session, customer: customer_schemas.CustomerCreate):
    """
    Create a new customer in the database.

    Args:
        db (Session): Database session.
        customer (customer_schemas.CustomerCreate): Customer data to create.

    Returns:
        models.Customer: The created customer with its ID.
    """
    customer.password = password_hash(customer.password)
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customer(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of customers with pagination.

    Args:
        db (Session): Database session.
        skip (int, optional): Number of customers to skip. Defaults to 0.
        limit (int, optional): Maximum number of customers to return. Defaults to 10.

    Returns:
        list[models.Customer]: List of customers with is_admin properly set.
    """
    customers = db.query(models.Customer).offset(skip).limit(limit).all()
    # Ensure is_admin is always a boolean
    for customer in customers:
        if customer.is_admin is None:
            customer.is_admin = False
    return customers


def get_customer_by_id(db: Session, customer_id: int):
    """
    Retrieve a customer by ID.

    Args:
        db (Session): Database session.
        customer_id (int): ID of the customer to retrieve.

    Returns:
        models.Customer: The requested customer with is_admin properly set, or None if not found.
    """
    customer = db.query(models.Customer).filter(models.Customer.c_id == customer_id).first()
    if customer and customer.is_admin is None:
        customer.is_admin = False
    return customer


def update_customer(db: Session, customer_id: int, customer_data: customer_schemas.CustomerUpdate):
    """
    Update a customer's information.

    Args:
        db (Session): Database session.
        customer_id (int): ID of the customer to update.
        customer_data (customer_schemas.CustomerUpdate): New customer data.

    Returns:
        models.Customer: The updated customer, or None if not found.
    """
    db_customer = db.query(models.Customer).filter(models.Customer.c_id == customer_id).first()
    if db_customer:
        update_data = customer_data.model_dump()
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer
