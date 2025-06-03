from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app import models
from app.routers import oauth2
from app.schemas import customer as schemas
from app.utils.database import get_db
from app.utils.password import verify_password, password_hash

router = APIRouter()


@router.post("/register", response_model=schemas.Customer, status_code=status.HTTP_201_CREATED)
def customer_register(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """
    Register a new customer.

    This endpoint allows creating a new customer account.

    Args:
        customer (schemas.CustomerCreate): Customer data including email and password.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        schemas.Customer: The created customer with its ID.

    Raises:
        HTTPException: If the email is already registered.

    Example:
        ```
        # Request
        POST /api/register
        {
            "email": "user@example.com",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "address": "123 Main St, City"
        }

        # Response (201 Created)
        {
            "c_id": 1,
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "address": "123 Main St, City"
        }
        ```
    """
    # Check for existing email
    existing = (
        db.query(models.Customer)
        .filter(models.Customer.email == customer.email)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = password_hash(customer.password)
    customer.password = hashed_password

    # Create a new customer with is_admin explicitly set to False
    customer_data = customer.model_dump()
    new_customer = models.Customer(**customer_data, is_admin=False)

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


@router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
def customer_login(
    user_cred: schemas.CustomerLogin, db: Session = Depends(get_db)
):
    """
    Customer login.

    This endpoint authenticates a customer and returns an access token.
    The token should be included in the Authorization header for subsequent requests.

    Args:
        user_cred (schemas.CustomerLogin): Customer credentials (email and password).
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If the email doesn't exist or the password is incorrect.

    Example:
        ```
        # Request
        POST /api/login
        {
            "email": "user@example.com",
            "password": "securepassword123"
        }

        # Response (200 OK)
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }

        # Usage in subsequent requests
        GET /api/customers/1
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        ```
    """
    # Email validation is handled by Pydantic's EmailStr
    # Additional validation can be added here if needed

    # Check if email exists in the database
    customer = (
        db.query(models.Customer)
        .filter(models.Customer.email == user_cred.email)
        .first()
    )
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # Validate password
    if not verify_password(user_cred.password, customer.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password"
        )

    # Generate access token
    access_token = oauth2.create_access_token(data={"customer_id": customer.c_id})
    return {"access_token": access_token, "token_type": "bearer"}
