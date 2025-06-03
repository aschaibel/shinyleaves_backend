from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class TokenData(BaseModel):
    """
    Schema for JWT token data.

    Contains the customer ID extracted from a JWT token.

    Attributes:
        id (Optional[int]): The customer ID, can be None if not provided.
    """
    id: Optional[int] = None


class CustomerBase(BaseModel):
    """
    Base schema for customer data.

    Contains the common fields used across different customer schemas.

    Attributes:
        name (str): Customer's full name.
        address (str): Customer's physical address.
        email (str): Customer's email address.
        password (str): Customer's password.
    """
    name: str
    address: str
    email: str
    password: str


class CustomerCreate(CustomerBase):
    """
    Schema for creating a new customer.

    Extends CustomerBase with validated email field.

    Attributes:
        email (EmailStr): Customer's email address, validated as a proper email format.
        password (str): Customer's password.
    """
    email: EmailStr
    password: str


class Customer(CustomerBase):
    """
    Schema for customer response data.

    Extends CustomerBase with ID and admin status. Used for API responses.

    Attributes:
        c_id (int): Customer ID, aliased as "id" in API responses.
        is_admin (bool): Flag indicating whether the customer has admin privileges. Defaults to False.
    """
    c_id: int = Field(alias="id")
    is_admin: bool = False

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }


class CustomerLogin(BaseModel):
    """
    Schema for customer login credentials.

    Used for authenticating customers in the login endpoint.

    Attributes:
        email (EmailStr): Customer's email address, validated as a proper email format.
        password (str): Customer's password.
    """
    email: EmailStr
    password: str
