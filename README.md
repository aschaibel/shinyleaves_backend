---
> ⚠️ This project is for educational/demo purposes only. Follow local laws regarding cannabis sales and distribution.
---

# 🌿 ShinyLeaves Backend

**ShinyLeaves** is a modern, secure, and user-friendly online cannabis store. Designed with style and simplicity in mind, it allows users to browse premium strains, shop accessories, and enjoy a seamless checkout experience — all from the comfort of home.

This repository contains the backend API for the ShinyLeaves application, built with FastAPI and SQLAlchemy.

---

## 🚀 Features

- 🌱 Product catalog with detailed strain descriptions
- 🔍 Smart search and filtering by effects, type, and THC/CBD levels
- 🛒 Smooth cart and checkout flow
- 🔐 Secure authentication and age verification
- 📦 Order tracking and history
- 🎨 Sleek, responsive design (mobile-first)

---

## 🧰 Tech Stack

- **Backend Framework:** FastAPI
- **Database ORM:** SQLAlchemy
- **Database:** MySQL
- **API Documentation:** OpenAPI/Swagger
- **Authentication:** JWT
- **Containerization:** Docker & Docker Compose
- **Validation:** Pydantic

---

## 🛠️ Setup and Installation

### Prerequisites
- Docker and Docker Compose
- Python 3.8+

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/shinyleaves_backend.git
   cd shinyleaves_backend
   ```

2. **Set up a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the application with Docker Compose**
   ```bash
   docker-compose up -d
   ```

5. **Access the API**
   - API: http://localhost:8000/api
   - API Documentation: http://localhost:8000/docs

### Environment Variables

The application uses the following environment variables:

#### Required Environment Variables

- `DATABASE_URL`: Database connection string (if provided, overrides individual components)
- `SECRET_KEY`: Secret key for JWT token generation
- `ALGORITHM`: Algorithm used for JWT token generation (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes

#### Optional Environment Variables

- `API_PREFIX`: Prefix for all API endpoints (default: `/api`)
- `DEBUG`: Enable debug mode (default: `False`)
- `CORS_ORIGINS`: Allowed origins for CORS (default: `["*"]`)
- `HOST`: Host to bind the server to (default: `0.0.0.0`)
- `PORT`: Port to bind the server to (default: `8000`)

For more detailed information about environment variables, see [Environment Variables Documentation](docs/environment_variables.md).

---

## 📁 Project Structure

```
shinyleaves_backend/
├── app/                    # Application code
│   ├── crud/               # CRUD operations for database entities
│   ├── models/             # SQLAlchemy models
│   ├── routers/            # API routes
│   ├── schemas/            # Pydantic schemas for validation
│   ├── utils/              # Utility functions and classes
│   └── main.py             # Application entry point
├── data/                   # Database data (when using Docker)
├── db/                     # Database initialization scripts
├── docs/                   # Documentation
├── tests/                  # Test cases
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker configuration
└── README.md               # Project documentation
```

---

## 🔄 API Endpoints

The API provides the following endpoints:

### Authentication
- `POST /api/login`: User login
- `POST /api/register`: User registration

### Products
- `GET /api/products/`: Get list of products with pagination
- `GET /api/products/{product_id}`: Get product by ID
- `POST /api/products/`: Create multiple products (admin only)
- `PATCH /api/products/{product_id}`: Update product (admin only)
- `DELETE /api/products/{product_id}`: Delete product (admin only)

### Orders
- `GET /api/orders/`: Get list of orders with pagination
- `GET /api/orders/{order_id}`: Get order by ID
- `POST /api/order/`: Create new order
- `PATCH /api/orders/{order_id}`: Update order
- `DELETE /api/orders/{order_id}`: Delete order

### Customers
- `GET /api/customers/`: Get list of customers with pagination (admin only)
- `GET /api/customers/{customer_id}`: Get customer by ID (users can access their own data, admins can access any customer's data)
- `GET /api/customers/me`: Get the current logged-in customer's information
- `POST /api/customers/`: Create new customer
- `PATCH /api/customers/{customer_id}`: Update customer
- `PATCH /api/customers/me`: Update the current customer's name and address
- `DELETE /api/customers/{customer_id}`: Delete customer

### Additional Features

- **Pagination**: List endpoints support pagination with `skip` and `limit` query parameters
- **Rate Limiting**: To prevent abuse, the API implements rate limiting
- **Authentication**: The API uses JWT (JSON Web Tokens) for authentication

For detailed API documentation, visit the Swagger UI at http://localhost:8000/docs when the application is running, or see the [API Documentation](docs/api_documentation.md).

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app
```

---

## 📫 Contact

Got questions or feedback? Reach out:

* 🌐 Website: [shinyleaves.io](https://shinyleaves.io)
* 📧 Email: [support@shinyleaves.io](mailto:support@shinyleaves.io)
* 🐦 Twitter: [@shinyleaves](https://twitter.com/shinyleaves)

---

*ShinyLeaves — Elevate your experience.*
