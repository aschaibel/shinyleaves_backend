from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import models
from app.schemas import customer as schemas
from app.utils.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

SECRET_KEY = "123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """
    Create a new JWT access token.

    Args:
        data (dict): The data to encode in the token, typically contains customer_id.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """
    Verify and decode a JWT access token.

    Args:
        token (str): The JWT token to verify.
        credentials_exception (HTTPException): Exception to raise if verification fails.

    Returns:
        schemas.TokenData: The decoded token data containing the customer ID.

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
    Get the current authenticated user from the JWT token.

    This dependency can be used in route functions to get the current authenticated user.

    Args:
        token (str, optional): The JWT token from the Authorization header. Defaults to Depends(oauth2_scheme).
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        models.Customer: The authenticated customer.

    Raises:
        HTTPException: If the token is invalid or the customer doesn't exist.
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


def get_admin_user(current_user: models.Customer = Depends(get_current_user)):
    """
    Verify that the current user has admin privileges.

    This dependency can be used in route functions that require admin access.

    Args:
        current_user (models.Customer, optional): The authenticated customer. Defaults to Depends(get_current_user).

    Returns:
        models.Customer: The authenticated admin customer.

    Raises:
        HTTPException: If the user doesn't have admin privileges.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action. Admin privileges required.",
        )
    return current_user
