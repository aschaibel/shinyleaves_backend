from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import models
from app.schemas import customer as schemas
from app.utils.database import get_db

# Configure OAuth2 with Password flow, pointing to our login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# JWT Configuration
# Note: In production, SECRET_KEY should be a strong, random value stored securely
SECRET_KEY = "123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """
    Create a JWT access token.

    This function creates a JWT token with the provided data and an expiration time.
    The token is used for authenticating API requests.

    Args:
        data (dict): The data to encode in the token, typically contains user identification.

    Returns:
        str: The encoded JWT token.

    Example:
        ```python
        # Creating a token for a customer with ID 1
        token = create_access_token(data={"customer_id": 1})
        # Returns: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        ```
    """
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """
    Verify a JWT access token.

    This function decodes and validates a JWT token, extracting the customer ID.

    Args:
        token (str): The JWT token to verify.
        credentials_exception (HTTPException): Exception to raise if verification fails.

    Returns:
        schemas.TokenData: Object containing the customer ID from the token.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        customer_id: str = payload.get("customer_id")
        if customer_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=customer_id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Get the current authenticated user.

    This function extracts the current user from the provided JWT token.
    It is typically used as a dependency in protected endpoints to ensure
    that only authenticated users can access them.

    Args:
        token (str, optional): JWT token from the Authorization header. 
            Defaults to Depends(oauth2_scheme).
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        models.Customer: The authenticated customer object.

    Raises:
        HTTPException: If the token is invalid or the user doesn't exist.

    Example:
        ```python
        # Using this function as a dependency in a protected endpoint
        @router.get("/protected-resource")
        def get_protected_resource(current_user: models.Customer = Depends(get_current_user)):
            # Only authenticated users can access this endpoint
            # The current_user parameter contains the authenticated customer's data
            return {"message": f"Hello, {current_user.first_name}!"}
        ```

    Usage in API requests:
        To access protected endpoints, include the JWT token in the Authorization header:
        ```
        GET /api/protected-resource
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        ```
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)

    customer = (
        db.query(models.Customer).filter(models.Customer.c_id == token.id).first()
    )

    return customer
