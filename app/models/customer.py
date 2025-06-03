from sqlalchemy import Column, Integer, String, Boolean

from app.utils.database import Base


class Customer(Base):
    """
    SQLAlchemy model for the customer table.

    Represents a customer in the system with personal information and authentication details.

    Attributes:
        c_id (int): Primary key, auto-incremented customer ID.
        name (str): Customer's full name.
        address (str): Customer's physical address.
        email (str): Customer's email address (unique).
        password (str): Customer's hashed password.
        is_admin (bool): Flag indicating whether the customer has admin privileges.
    """
    __tablename__ = "customer"

    c_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
