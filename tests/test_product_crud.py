import pytest
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.crud import product as product_crud
from app.schemas import product as product_schemas
from app.models.product import Product

def test_create_product(test_db):
    """Test creating a product."""
    # Create product data
    product_data = product_schemas.ProductCreate(
        name="Test Product",
        price=10.99,
        genetic="Indica",
        thc=20.0,
        cbd=5.0,
        effect="Relaxing",
        slug="test-product.jpg"
    )

    # Create product in database
    db_product = product_crud.create_product(db=test_db, product=product_data)

    # Check that product was created with correct data
    assert db_product.name == "Test Product"
    assert db_product.price == 10.99
    assert db_product.genetic == "Indica"
    assert db_product.thc == 20.0
    assert db_product.cbd == 5.0
    assert db_product.effect == "Relaxing"
    assert db_product.slug == "test-product.jpg"
    assert db_product.p_id is not None

def test_create_product_validation_error(test_db):
    """Test validation errors when creating a product."""
    # Test empty name
    product_data = product_schemas.ProductCreate(
        name="",
        price=10.99,
        genetic="Indica",
        thc=20.0,
        cbd=5.0,
        effect="Relaxing",
        slug="test-product.jpg"
    )

    with pytest.raises(HTTPException) as excinfo:
        product_crud.create_product(db=test_db, product=product_data)
    assert excinfo.value.status_code == 400
    assert "Name cannot be empty" in excinfo.value.detail

    # Test negative price
    product_data = product_schemas.ProductCreate(
        name="Test Product",
        price=-10.99,
        genetic="Indica",
        thc=20.0,
        cbd=5.0,
        effect="Relaxing",
        slug="test-product.jpg"
    )

    with pytest.raises(HTTPException) as excinfo:
        product_crud.create_product(db=test_db, product=product_data)
    assert excinfo.value.status_code == 400
    assert "Price must be greater than zero" in excinfo.value.detail

def test_get_products(test_db):
    """Test retrieving products with pagination."""
    # Create multiple products
    for i in range(5):
        product = Product(
            name=f"Product {i}",
            price=10.99 + i,
            genetic=f"Genetic {i}",
            thc=20.0 + i,
            cbd=5.0 + i,
            effect=f"Effect {i}",
            slug=f"product-{i}.jpg"
        )
        test_db.add(product)
    test_db.commit()

    # Test getting all products
    products = product_crud.get_products(db=test_db)
    assert len(products) == 5

    # Test pagination - skip 2, limit 2
    products_paginated = product_crud.get_products(db=test_db, skip=2, limit=2)
    assert len(products_paginated) == 2
    assert products_paginated[0].name == "Product 2"
    assert products_paginated[1].name == "Product 3"

def test_get_product_by_id(test_db):
    """Test retrieving a product by ID."""
    # Create a product
    product = Product(
        name="Test Product",
        price=10.99,
        genetic="Indica",
        thc=20.0,
        cbd=5.0,
        effect="Relaxing",
        slug="test-product.jpg"
    )
    test_db.add(product)
    test_db.commit()
    test_db.refresh(product)

    # Get product by ID
    db_product = product_crud.get_product_by_id(db=test_db, p_id=product.p_id)

    # Check that correct product was retrieved
    assert db_product is not None
    assert db_product.p_id == product.p_id
    assert db_product.name == product.name
    assert db_product.price == product.price

    # Test getting non-existent product
    with pytest.raises(ValueError) as excinfo:
        product_crud.get_product_by_id(db=test_db, p_id=999)
    assert "does not exist" in str(excinfo.value)

    # Test invalid ID type
    with pytest.raises(ValueError) as excinfo:
        product_crud.get_product_by_id(db=test_db, p_id="invalid")
    assert "must be an integer" in str(excinfo.value)

def test_update_product(test_db):
    """Test updating a product."""
    # Create a product
    product = Product(
        name="Original Product",
        price=10.99,
        genetic="Indica",
        thc=20.0,
        cbd=5.0,
        effect="Relaxing",
        slug="original-product.jpg"
    )
    test_db.add(product)
    test_db.commit()
    test_db.refresh(product)

    # Update product
    update_data = product_schemas.ProductUpdate(
        name="Updated Product",
        price=15.99,
        genetic="Indica",  # Same as original
        thc=20.0,          # Same as original
        cbd=5.0,           # Same as original
        effect="Relaxing", # Same as original
        slug="original-product.jpg"  # Same as original
    )
    updated_product = product_crud.update_products(
        db=test_db, 
        p_id=product.p_id, 
        update_data=update_data
    )

    # Check that product was updated correctly
    assert updated_product is not None
    assert updated_product.name == "Updated Product"
    assert updated_product.price == 15.99
    assert updated_product.genetic == "Indica"  # Unchanged

    # Test updating non-existent product
    result = product_crud.update_products(
        db=test_db, 
        p_id=999, 
        update_data=update_data
    )
    assert result is None

def test_delete_product(test_db):
    """Test deleting a product."""
    # Create a product
    product = Product(
        name="Product to Delete",
        price=10.99,
        genetic="Indica",
        thc=20.0,
        cbd=5.0,
        effect="Relaxing",
        slug="delete-product.jpg"
    )
    test_db.add(product)
    test_db.commit()
    test_db.refresh(product)

    # Delete product
    result = product_crud.delete_product_by_id(db=test_db, p_id=product.p_id)

    # Check that product was deleted
    assert result["status_code"] == 204
    assert "deleted successfully" in result["detail"]

    # Verify product no longer exists
    with pytest.raises(ValueError) as excinfo:
        product_crud.get_product_by_id(db=test_db, p_id=product.p_id)
    assert "does not exist" in str(excinfo.value)

    # Test deleting non-existent product
    with pytest.raises(HTTPException) as excinfo:
        product_crud.delete_product_by_id(db=test_db, p_id=999)
    assert excinfo.value.status_code == 404
    assert "Product not found" in excinfo.value.detail
