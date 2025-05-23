from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    """
    Base Pydantic model for product validation.

    This model defines the base fields for products without any validation rules.
    It is used as a base class for other product-related Pydantic models.

    Attributes:
        name (str): Name of the product.
        price (float): Price of the product.
        genetic (str): Genetic information of the weed.
        thc (float): THC content of the weed.
        cbd (float): CBD content of the weed.
        effect (str): Effect of the weed.
        slug (Optional[str]): Path to the product picture (optional).
    """
    name: str
    price: float
    genetic: str
    thc: float
    cbd: float
    effect: str
    slug: Optional[str] = None


class ProductCreate(ProductBase):
    """
    Pydantic model for creating a new product.

    This model inherits all fields from ProductBase and is used for validating
    data when creating a new product. It doesn't add any additional fields.

    Attributes:
        Inherits all attributes from ProductBase.
    """
    pass


class ProductUpdate(BaseModel):
    """
    Pydantic model for updating an existing product.

    This model defines the fields that can be updated for an existing product.
    All fields are optional, allowing partial updates.

    Attributes:
        name (Optional[str]): Updated name of the product (optional).
        price (Optional[float]): Updated price of the product (optional).
        genetic (Optional[str]): Updated genetic information of the weed (optional).
        thc (Optional[float]): Updated THC content of the weed (optional).
        cbd (Optional[float]): Updated CBD content of the weed (optional).
        effect (Optional[str]): Updated effect of the weed (optional).
        slug (Optional[str]): Updated path to the product picture (optional).
    """
    name: Optional[str]
    price: Optional[float]
    genetic: Optional[str]
    thc: Optional[float]
    cbd: Optional[float]
    effect: Optional[str]
    slug: Optional[str]


class Product(ProductBase):
    """
    Pydantic model for a complete product.

    This model represents a complete product with all fields, including the ID.
    It is used for returning product data from the API.

    Attributes:
        Inherits all attributes from ProductBase.
        p_id (int): Unique identifier for the product.
    """
    p_id: int

    model_config = {"from_attributes": True}
