# ShinyLeaves Architecture Documentation

This document provides an overview of the ShinyLeaves backend architecture, explaining the different components and how they interact with each other.

## Architecture Overview

ShinyLeaves follows a layered architecture pattern, which separates concerns and makes the codebase more maintainable and testable. The main layers are:

1. **API Layer (Routers)**: Handles HTTP requests and responses
2. **Business Logic Layer (CRUD)**: Implements business logic and data manipulation
3. **Data Access Layer (Models)**: Defines database models and handles database interactions
4. **Schema Layer**: Defines data validation and serialization/deserialization

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Applications                       │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                           FastAPI App                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                      API Layer (Routers)                 │   │
│  │                                                         │   │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐  │   │
│  │  │ Product │   │  Weed   │   │ Orders  │   │Customer │  │   │
│  │  │ Router  │   │ Router  │   │ Router  │   │ Router  │  │   │
│  │  └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘  │   │
│  └───────┼──────────────┼──────────────┼──────────────┼────┘   │
│          │              │              │              │        │
│          ▼              ▼              ▼              ▼        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │               Business Logic Layer (CRUD)                │   │
│  │                                                         │   │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐  │   │
│  │  │ Product │   │  Weed   │   │ Orders  │   │Customer │  │   │
│  │  │  CRUD   │   │  CRUD   │   │  CRUD   │   │  CRUD   │  │   │
│  │  └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘  │   │
│  └───────┼──────────────┼──────────────┼──────────────┼────┘   │
│          │              │              │              │        │
│          ▼              ▼              ▼              ▼        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Data Access Layer (Models)               │   │
│  │                                                         │   │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐  │   │
│  │  │ Product │   │  Weed   │   │ Orders  │   │Customer │  │   │
│  │  │  Model  │   │  Model  │   │  Model  │   │  Model  │  │   │
│  │  └─────────┘   └─────────┘   └─────────┘   └─────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     Schema Layer                         │   │
│  │                                                         │   │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐  │   │
│  │  │ Product │   │  Weed   │   │ Orders  │   │Customer │  │   │
│  │  │ Schema  │   │ Schema  │   │ Schema  │   │ Schema  │  │   │
│  │  └─────────┘   └─────────┘   └─────────┘   └─────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     Utility Layer                        │   │
│  │                                                         │   │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────────────────┐   │   │
│  │  │Database │   │  Auth   │   │Other Utility Classes│   │   │
│  │  │ Utils   │   │  Utils  │   │    and Functions    │   │   │
│  │  └─────────┘   └─────────┘   └─────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                           Database                              │
└─────────────────────────────────────────────────────────────────┘
```

## Layer Descriptions

### 1. API Layer (Routers)

The API layer is responsible for handling HTTP requests and responses. It defines the API endpoints and their behavior.

**Key Components:**
- **Router Modules**: Define API endpoints for different resources (products, weed, orders, customers, auth)
- **Request Handling**: Parse request parameters, body, and headers
- **Response Formatting**: Format responses according to API specifications
- **Error Handling**: Handle and format errors that occur during request processing
- **Authentication**: Verify user credentials and permissions

**Example (from product.py router):**
```python
@router.get("/products/", response_model=list[schemas.Product])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_products(db=db, skip=skip, limit=limit)
```

### 2. Business Logic Layer (CRUD)

The business logic layer implements the application's business logic and data manipulation operations.

**Key Components:**
- **CRUD Operations**: Create, Read, Update, Delete operations for different resources
- **Business Rules**: Implement business rules and validations
- **Transaction Management**: Manage database transactions
- **Error Handling**: Handle and propagate errors that occur during business operations

**Example (from product.py CRUD):**
```python
def create_product(db: Session, product: product_schemas.ProductCreate):
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
        # Error handling...
```

### 3. Data Access Layer (Models)

The data access layer defines the database models and handles database interactions.

**Key Components:**
- **SQLAlchemy Models**: Define database tables and their relationships
- **Database Operations**: Perform database operations using SQLAlchemy ORM
- **Data Mapping**: Map database records to application objects

**Example (from product.py model):**
```python
class Product(Base):
    __tablename__ = "product"
    p_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    w_id = Column(Integer, ForeignKey("weed.w_id"), nullable=False)
    slug = Column(String(255), nullable=True)
```

### 4. Schema Layer

The schema layer defines data validation and serialization/deserialization using Pydantic models.

**Key Components:**
- **Pydantic Models**: Define data validation and serialization/deserialization
- **Input Validation**: Validate input data according to defined schemas
- **Output Formatting**: Format output data according to defined schemas

**Example (from product.py schema):**
```python
class ProductBase(BaseModel):
    name: str
    price: float
    w_id: int
    slug: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    p_id: int
    model_config = {"from_attributes": True}
```

### 5. Utility Layer

The utility layer provides common functionality used across the application.

**Key Components:**
- **Database Utilities**: Database connection and session management
- **Authentication Utilities**: JWT token generation and validation
- **Other Utilities**: Common functions and classes used across the application

**Example (from database.py):**
```python
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@db:3306/shinyleaves"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Request Flow

1. **Client Request**: A client sends an HTTP request to the API
2. **Router**: The appropriate router handles the request based on the URL and HTTP method
3. **Input Validation**: The request data is validated using Pydantic schemas
4. **Business Logic**: The router calls the appropriate CRUD function to perform the business logic
5. **Database Interaction**: The CRUD function interacts with the database using SQLAlchemy models
6. **Response**: The result is serialized using Pydantic schemas and returned to the client

## Authentication Flow

1. **Login Request**: A client sends login credentials to the `/api/auth/login` endpoint
2. **Credential Verification**: The auth router verifies the credentials against the database
3. **Token Generation**: If the credentials are valid, a JWT token is generated and returned to the client
4. **Authenticated Requests**: The client includes the JWT token in subsequent requests
5. **Token Verification**: The API verifies the token for protected endpoints
6. **Access Control**: The API grants or denies access based on the token's validity and permissions

## Deployment Architecture

The application is deployed using Docker and Docker Compose, which provides the following benefits:
- **Isolation**: Each component runs in its own container
- **Portability**: The application can be easily deployed to different environments
- **Scalability**: The application can be scaled horizontally by adding more containers
- **Dependency Management**: Dependencies are managed within containers

The deployment consists of the following containers:
- **Backend Container**: Runs the FastAPI application
- **Database Container**: Runs the MySQL database

## Future Architecture Improvements

Based on the tasks.md file, the following architecture improvements are planned:
- **Service Layer**: Add a service layer between CRUD and router layers
- **Dependency Injection**: Implement proper dependency injection for services
- **Configuration Management**: Add a configuration management system with environment-specific configs
- **Logging System**: Implement a logging system with different log levels
- **Caching**: Implement a caching mechanism for frequently accessed data
- **Database Migrations**: Implement database migrations using Alembic
- **Health Checks**: Add health check endpoints for monitoring