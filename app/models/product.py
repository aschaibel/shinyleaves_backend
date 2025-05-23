from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Float

from app.utils.database import Base


class Product(Base):
    """
    SQLAlchemy model for the product table.

    This model represents a product in the database. Each product has a unique ID,
    a name, a price, weed-related attributes (genetic, thc, cbd, effect), and an optional slug for the product image.

    Attributes:
        p_id (int): Primary key for the product table.
        name (str): Name of the product.
        price (float): Price of the product.
        genetic (str): Genetic information of the weed.
        thc (float): THC content of the weed.
        cbd (float): CBD content of the weed.
        effect (str): Effect of the weed.
        slug (str): Path to the product picture (optional).
    """
    __tablename__ = "product"
    p_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    genetic = Column(String(255), nullable=False)
    thc = Column(Float, nullable=False)
    cbd = Column(Float, nullable=False)
    effect = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=True)


class ProductBase(BaseModel):
    """
    Base Pydantic model for product validation.

    This model defines the base fields and validation rules for products.
    It is used as a base class for other product-related Pydantic models.

    Attributes:
        name (str): Name of the product. Must be between 1 and 255 characters.
        price (float): Price of the product. Must be greater than 0.
        w_id (int): Foreign key to the weed table.
        slug (str): Path to the product picture (optional).
    """
    name: str = Field(
        ..., min_length=1, max_length=255, description="Name cannot be empty"
    )
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    w_id: int
    slug: str = Field(None, description="Path to the product picture")
