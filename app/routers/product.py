from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.crud import product as crud
from app.crud.product import delete_product_by_id
from app.models.customer import Customer
from app.routers.oauth2 import get_admin_user
from app.schemas import product as schemas
from app.utils.database import get_db

router = APIRouter()


@router.post("/products/", response_model=List[schemas.Product])
def create_products(
    product: List[schemas.ProductCreate], 
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_admin_user)
):
    """
    Create multiple products.

    This endpoint allows creating multiple products in a single request.
    Requires admin privileges.

    Args:
        product (List[schemas.ProductCreate]): List of products to create.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (Customer): The authenticated admin user.

    Returns:
        List[schemas.Product]: List of created products with their IDs.
    """
    return [crud.create_product(db=db, product=p) for p in product]


@router.get("/products/", response_model=list[schemas.Product])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get a list of products with pagination.

    This endpoint returns a paginated list of products.

    Args:
        skip (int, optional): Number of products to skip. Defaults to 0.
        limit (int, optional): Maximum number of products to return. Defaults to 10.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        list[schemas.Product]: List of products.
    """
    return crud.get_products(db=db, skip=skip, limit=limit)

@router.get("/products/{product_id}", response_model=schemas.Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """
    Get a product by ID.

    This endpoint returns a single product by its ID.

    Args:
        product_id (int): ID of the product to retrieve.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        schemas.Product: The requested product.

    Raises:
        HTTPException: If a database error occurs or the product is not found.
    """
    try:
        return crud.get_product_by_id(db=db, p_id=product_id)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occured while getting product id."
        )


@router.patch("/products/{product_id}", response_model=schemas.Product)
def patch_product_by_id(
    product_id: int, 
    update_data: schemas.ProductUpdate, 
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_admin_user)
):
    """
    Update a product.

    This endpoint allows partial updates to a product.
    Requires admin privileges.

    Args:
        product_id (int): ID of the product to update.
        update_data (schemas.ProductUpdate): Data to update the product with.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (Customer): The authenticated admin user.

    Returns:
        schemas.Product: The updated product.

    Raises:
        HTTPException: If the product is not found.
    """
    product = crud.update_products(db, product_id, update_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/products/{product_id}")
async def remove_product_by_id(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_admin_user)
):
    """
    Delete a product.

    This endpoint deletes a product by its ID.
    Requires admin privileges.

    Args:
        product_id (int): ID of the product to delete.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (Customer): The authenticated admin user.

    Returns:
        Response: Empty response with 204 status code if successful.

    Raises:
        HTTPException: If the product is not found or a database error occurs.
    """
    delete_product_by_id(db, product_id)
    return Response(status_code=204)
