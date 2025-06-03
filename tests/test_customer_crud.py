import pytest
from app.crud import customer as customer_crud
from app.schemas import customer as customer_schemas
from app.models.customer import Customer

def test_create_customer(test_db):
    """Test creating a customer."""
    # Create customer data
    customer_data = customer_schemas.CustomerCreate(
        name="New User",
        address="456 New St",
        email="new@example.com",
        password="password123"
    )
    
    # Create customer in database
    db_customer = customer_crud.create_customer(db=test_db, customer=customer_data)
    
    # Check that customer was created with correct data
    assert db_customer.name == "New User"
    assert db_customer.address == "456 New St"
    assert db_customer.email == "new@example.com"
    assert db_customer.password != "password123"  # Password should be hashed
    assert db_customer.is_admin is False
    assert db_customer.c_id is not None

def test_get_customer(test_db, test_customer):
    """Test retrieving customers with pagination."""
    # Create additional customers
    for i in range(5):
        customer = Customer(
            name=f"User {i}",
            address=f"{i} Test St",
            email=f"user{i}@example.com",
            password=f"password{i}",
            is_admin=False
        )
        test_db.add(customer)
    test_db.commit()
    
    # Test getting all customers
    customers = customer_crud.get_customer(db=test_db)
    assert len(customers) == 6  # 5 new customers + 1 test_customer
    
    # Test pagination - skip 2, limit 2
    customers_paginated = customer_crud.get_customer(db=test_db, skip=2, limit=2)
    assert len(customers_paginated) == 2
    
    # Test is_admin is always a boolean
    for customer in customers:
        assert isinstance(customer.is_admin, bool)

def test_get_customer_by_id(test_db, test_customer):
    """Test retrieving a customer by ID."""
    # Get customer by ID
    db_customer = customer_crud.get_customer_by_id(db=test_db, customer_id=test_customer.c_id)
    
    # Check that correct customer was retrieved
    assert db_customer is not None
    assert db_customer.c_id == test_customer.c_id
    assert db_customer.name == test_customer.name
    assert db_customer.email == test_customer.email
    
    # Test getting non-existent customer
    non_existent = customer_crud.get_customer_by_id(db=test_db, customer_id=999)
    assert non_existent is None
    
    # Test is_admin is always a boolean
    assert isinstance(db_customer.is_admin, bool)

def test_get_customer_by_id_with_null_is_admin(test_db):
    """Test that is_admin is set to False if it's None."""
    # Create a customer with is_admin=None
    customer = Customer(
        name="Admin Test",
        address="Admin St",
        email="admin@example.com",
        password="admin_password",
        is_admin=None  # Explicitly set to None
    )
    test_db.add(customer)
    test_db.commit()
    test_db.refresh(customer)
    
    # Get customer by ID
    db_customer = customer_crud.get_customer_by_id(db=test_db, customer_id=customer.c_id)
    
    # Check that is_admin is False, not None
    assert db_customer.is_admin is False