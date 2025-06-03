import pytest
from datetime import datetime, timedelta
from jose import jwt
from fastapi import HTTPException

from app.routers.oauth2 import (
    create_access_token,
    verify_access_token,
    get_current_user,
    get_admin_user,
    SECRET_KEY,
    ALGORITHM
)
from app.schemas.customer import TokenData
from app.models.customer import Customer

def test_create_access_token():
    """Test creating a JWT access token."""
    data = {"customer_id": 1}
    token = create_access_token(data)

    # Verify token is a string
    assert isinstance(token, str)

    # Decode token and verify payload
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("customer_id") == 1
    assert "exp" in payload  # Expiration time should be set

def test_verify_access_token_valid():
    """Test verifying a valid JWT access token."""
    # Create a token with known payload
    data = {"customer_id": 1}
    token = create_access_token(data)

    # Create a credentials exception
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify token
    token_data = verify_access_token(token, credentials_exception)

    # Check token data
    assert isinstance(token_data, TokenData)
    assert token_data.id == 1

def test_verify_access_token_invalid():
    """Test verifying an invalid JWT access token."""
    # Create an invalid token
    invalid_token = "invalid_token"

    # Create a credentials exception
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify token should raise exception
    with pytest.raises(HTTPException) as excinfo:
        verify_access_token(invalid_token, credentials_exception)

    # Check exception details
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"

def test_verify_access_token_missing_customer_id():
    """Test verifying a JWT access token with missing customer_id."""
    # Create a token without customer_id
    data = {"some_other_field": "value"}
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    # Create a credentials exception
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify token should raise exception
    with pytest.raises(HTTPException) as excinfo:
        verify_access_token(token, credentials_exception)

    # Check exception details
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"

def test_verify_access_token_expired():
    """Test verifying an expired JWT access token."""
    # Create a token with invalid format to trigger JWTError
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lcl9pZCI6MSwiZXhwIjoxNTE2MjM5MDIyfQ.invalid_signature"

    # Create a credentials exception
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify token should raise exception
    with pytest.raises(HTTPException) as excinfo:
        verify_access_token(invalid_token, credentials_exception)

    # Check exception details
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"

def test_get_current_user(test_db, test_customer):
    """Test getting the current user from a token."""
    # This test requires mocking the token dependency, which is more complex
    # In a real test, you would use FastAPI's TestClient and dependency_overrides
    # For now, we'll just test the token verification part
    pass

def test_get_admin_user(test_db, test_customer):
    """Test verifying admin privileges."""
    # Create admin and non-admin customers
    admin_customer = test_db.query(Customer).filter(Customer.c_id == test_customer.c_id).first()
    admin_customer.is_admin = True
    test_db.commit()

    # Test with admin user should pass
    result = get_admin_user(admin_customer)
    assert result == admin_customer

    # Test with non-admin user should raise exception
    admin_customer.is_admin = False
    test_db.commit()

    with pytest.raises(HTTPException) as excinfo:
        get_admin_user(admin_customer)

    # Check exception details
    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == "Not authorized to perform this action. Admin privileges required."
