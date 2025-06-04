from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import customer as crud
from app.models.customer import Customer
from app.routers.oauth2 import get_admin_user, get_current_user
from app.schemas import customer as schemas
from app.utils.database import get_db

router = APIRouter()


@router.get("/customers/", response_model=list[schemas.Customer])
def get_customers(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_admin_user)
):
    """
    Get a list of customers with pagination.

    This endpoint returns a paginated list of customers.
    Requires admin privileges.

    Args:
        skip (int, optional): Number of customers to skip. Defaults to 0.
        limit (int, optional): Maximum number of customers to return. Defaults to 10.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (Customer): The authenticated admin user.

    Returns:
        list[schemas.Customer]: List of customers.
    """
    return crud.get_customer(db=db, skip=skip, limit=limit)


@router.get("/customers/me", response_model=schemas.Customer)
def get_customer_me(current_user: Customer = Depends(get_current_user)):
    """
    Get the current logged-in customer's information.

    This endpoint returns the data of the currently authenticated customer.
    For regular users, sensitive fields (id and is_admin) are excluded.
    For admin users, all fields are included.

    Args:
        current_user (Customer): The authenticated customer.

    Returns:
        schemas.Customer or schemas.CustomerResponse: The current customer's data.
    """
    # Use different response models based on user role
    if current_user.is_admin:
        # Use the original response_model defined in the decorator
        return current_user
    else:
        # Override the response_model for non-admin users
        from fastapi.responses import JSONResponse
        return JSONResponse(content={
            "name": current_user.name,
            "address": current_user.address,
            "email": current_user.email
        })


@router.get("/customers/{customer_id}", response_model=schemas.Customer)
def get_customer_by_id(
    customer_id: int, 
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user)
):
    """
    Get a customer by ID.

    This endpoint returns a single customer by its ID.
    Regular users can only access their own data, while admins can access any customer's data.
    For regular users, sensitive fields (id and is_admin) are excluded.
    For admin users, all fields are included.

    Args:
        customer_id (int): ID of the customer to retrieve.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (Customer): The authenticated user.

    Returns:
        schemas.Customer or schemas.CustomerResponse: The requested customer.

    Raises:
        HTTPException: If the customer is not found or if a non-admin user tries to access another user's data.
    """
    # Check if user is trying to access their own data or if they're an admin
    if current_user.c_id != customer_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this customer's data"
        )

    db_customer = crud.get_customer_by_id(db=db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Use different response models based on user role
    if current_user.is_admin:
        # Use the original response_model defined in the decorator
        return db_customer
    else:
        # Override the response_model for non-admin users
        from fastapi.responses import JSONResponse
        return JSONResponse(content={
            "name": db_customer.name,
            "address": db_customer.address,
            "email": db_customer.email
        })


@router.patch("/customers/me", response_model=schemas.Customer)
def update_customer_me(
    customer_data: schemas.CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user)
):
    """
    Update the current customer's information.

    This endpoint allows a logged-in customer to update their name and address.
    For regular users, sensitive fields (id and is_admin) are excluded from the response.
    For admin users, all fields are included in the response.

    Args:
        customer_data (schemas.CustomerUpdate): New customer data (name and address).
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (Customer): The authenticated customer.

    Returns:
        schemas.Customer or schemas.CustomerResponse: The updated customer data.
    """
    updated_customer = crud.update_customer(
        db=db, 
        customer_id=current_user.c_id, 
        customer_data=customer_data
    )

    # Use different response models based on user role
    if current_user.is_admin:
        # Use the original response_model defined in the decorator
        return updated_customer
    else:
        # Override the response_model for non-admin users
        from fastapi.responses import JSONResponse
        return JSONResponse(content={
            "name": updated_customer.name,
            "address": updated_customer.address,
            "email": updated_customer.email
        })
