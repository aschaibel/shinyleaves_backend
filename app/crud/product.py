from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from app.models import product as models
from app.schemas import product as product_schemas


def create_product(db: Session, product: product_schemas.ProductCreate):
    """
    Create a new product in the database.

    This function creates a new product with the provided data. It performs validation
    on the input data and handles various error cases.

    Args:
        db (Session): Database session.
        product (product_schemas.ProductCreate): Product data to create.

    Returns:
        models.Product: The created product with its ID.

    Raises:
        HTTPException: If validation fails or a database error occurs.
    """
    if not product.name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if product.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than zero")

    db_product = models.Product(**product.model_dump())
    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    except IntegrityError as error:
        db.rollback()

        if hasattr(error.orig, "args") and error.orig.args[0] == 1452:
            raise HTTPException(
                status_code=400,
                detail="Cannot create product: referenced weed ID does not exist",
            )

        raise HTTPException(status_code=400, detail=f"Integrity: {str(error)}")
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unknown error: {str(error)}")


def get_products(db: Session, skip: int = 0, limit: int = 10):
    """
    Get a list of products with pagination.

    This function retrieves a paginated list of products from the database.

    Args:
        db (Session): Database session.
        skip (int, optional): Number of products to skip. Defaults to 0.
        limit (int, optional): Maximum number of products to return. Defaults to 10.

    Returns:
        list[models.Product]: List of products.
    """
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, p_id: int):
    """
    Get a product by ID.

    This function retrieves a single product by its ID.

    Args:
        db (Session): Database session.
        p_id (int): ID of the product to retrieve.

    Returns:
        models.Product: The requested product.

    Raises:
        ValueError: If p_id is not an integer or the product does not exist.
        RuntimeError: If a database error occurs.
    """
    try:
        if not isinstance(p_id, int):
            raise ValueError("p_id must be an integer")
        product = db.query(models.Product).filter(models.Product.p_id == p_id).first()
        if product is None:
            raise ValueError(f"Product with id {p_id} does not exist")
        return product
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to get product by id: {str(e)}")


def update_products(db: Session, p_id: int, update_data: product_schemas.ProductUpdate):
    """
    Update an existing product.

    This function updates an existing product with the provided data.

    Args:
        db (Session): Database session.
        p_id (int): ID of the product to update.
        update_data (product_schemas.ProductUpdate): Data to update the product with.

    Returns:
        models.Product: The updated product, or None if the product was not found.

    Raises:
        Exception: If a database error occurs during the update.
    """
    try:
        product = db.query(models.Product).filter(models.Product.p_id == p_id).first()
        if not product:
            return None

        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise Exception(f"Error updating product: {str(e)}")


def delete_product_by_id(db: Session, p_id: int):
    """
    Delete a product by ID.

    This function deletes a product from the database by its ID.

    Args:
        db (Session): Database session.
        p_id (int): ID of the product to delete.

    Returns:
        dict: Status code and message indicating successful deletion.

    Raises:
        HTTPException: If the product is not found or a database error occurs.
    """
    product_to_delete = (
        db.query(models.Product).filter(models.Product.p_id == p_id).first()
    )

    if not product_to_delete:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        db.delete(product_to_delete)
        db.commit()
        return {"status_code": 204, "detail": "Product deleted successfully"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database error during deletion: {str(e)}"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Unknown error during deletion: {str(e)}"
        )
