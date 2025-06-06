# ShinyLeaves API Documentation

This document provides information about the ShinyLeaves API, including how to access the auto-generated API documentation and examples of how to use the API.

## Accessing API Documentation

ShinyLeaves uses FastAPI's built-in support for OpenAPI and Swagger UI to provide interactive API documentation. When the application is running, you can access the documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces provide:
- A list of all available endpoints
- Request and response schemas
- The ability to try out API calls directly from the browser
- Authentication information

## API Endpoints Overview

The ShinyLeaves API is organized around the following resources:

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/products/ | Get a list of products with pagination |
| GET | /api/products/{product_id} | Get a product by ID |
| POST | /api/products/ | Create multiple products |
| PATCH | /api/products/{product_id} | Update a product |
| DELETE | /api/products/{product_id} | Delete a product |


### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/orders/ | Get a list of orders with pagination |
| GET | /api/orders/{order_id} | Get an order by ID |
| POST | /api/order/ | Create a new order |
| PATCH | /api/orders/{order_id} | Update an order |
| DELETE | /api/orders/{order_id} | Delete an order |

### Customers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/customers/ | Get a list of customers with pagination |
| GET | /api/customers/{customer_id} | Get a customer by ID (users can access their own data, admins can access any customer's data) |
| GET | /api/customers/me | Get the current logged-in customer's information |
| POST | /api/customers/ | Create a new customer |
| PATCH | /api/customers/{customer_id} | Update a customer |
| PATCH | /api/customers/me | Update the current customer's name and address |
| DELETE | /api/customers/{customer_id} | Delete a customer |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/login | User login |
| POST | /api/register | User registration |

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To authenticate:

1. Send a POST request to `/api/login` with your credentials
2. Receive a JWT token in the response
3. Include the token in the `Authorization` header of subsequent requests:
   ```
   Authorization: Bearer <your_token>
   ```

## Pagination

List endpoints support pagination with the following query parameters:

- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum number of items to return (default: 10)

Example: `/api/products/?skip=10&limit=5` will return products 11-15.

## Error Handling

The API returns appropriate HTTP status codes along with error messages:

- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

Error responses include a JSON object with a `detail` field containing the error message.

## API Examples

### Get Products

**Request:**
```http
GET /api/products/?skip=0&limit=5 HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
[
  {
    "p_id": 1,
    "name": "Premium Indica",
    "price": 29.99,
    "genetic": "Indica",
    "thc": 18.5,
    "cbd": 0.2,
    "effect": "Relaxing",
    "slug": "premium-indica"
  },
  {
    "p_id": 2,
    "name": "Sativa Delight",
    "price": 24.99,
    "genetic": "Sativa",
    "thc": 22.0,
    "cbd": 0.1,
    "effect": "Energizing",
    "slug": "sativa-delight"
  }
]
```

### Create a Product

**Request:**
```http
POST /api/products/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Bearer <your_token>

[
  {
    "name": "New Product",
    "price": 19.99,
    "genetic": "Hybrid",
    "thc": 20.0,
    "cbd": 0.5,
    "effect": "Balanced",
    "slug": "new-product"
  }
]
```

**Response:**
```json
[
  {
    "p_id": 3,
    "name": "New Product",
    "price": 19.99,
    "genetic": "Hybrid",
    "thc": 20.0,
    "cbd": 0.5,
    "effect": "Balanced",
    "slug": "new-product"
  }
]
```

### Update a Product

**Request:**
```http
PATCH /api/products/3 HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Bearer <your_token>

{
  "price": 22.99,
  "thc": 21.5
}
```

**Response:**
```json
{
  "p_id": 3,
  "name": "New Product",
  "price": 22.99,
  "genetic": "Hybrid",
  "thc": 21.5,
  "cbd": 0.5,
  "effect": "Balanced",
  "slug": "new-product"
}
```

### Delete a Product

**Request:**
```http
DELETE /api/products/3 HTTP/1.1
Host: localhost:8000
Authorization: Bearer <your_token>
```

**Response:**
```
204 No Content
```

### Get Customer by ID

**Request:**
```http
GET /api/customers/1 HTTP/1.1
Host: localhost:8000
Authorization: Bearer <your_token>
```

**Response:**
```json
{
  "id": 1,
  "name": "John Smith",
  "address": "123 Main Street, City, Country",
  "email": "john@example.com",
  "password": "hashed_password",
  "is_admin": false
}
```

### Get Current Customer

**Request:**
```http
GET /api/customers/me HTTP/1.1
Host: localhost:8000
Authorization: Bearer <your_token>
```

**Response:**
```json
{
  "id": 1,
  "name": "John Smith",
  "address": "123 Main Street, City, Country",
  "email": "john@example.com",
  "password": "hashed_password",
  "is_admin": false
}
```

### Update Current Customer

**Request:**
```http
PATCH /api/customers/me HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Bearer <your_token>

{
  "name": "John Smith",
  "address": "123 New Street, City, Country"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Smith",
  "address": "123 New Street, City, Country",
  "email": "john@example.com",
  "password": "hashed_password",
  "is_admin": false
}
```

## Rate Limiting

To prevent abuse, the API implements rate limiting. If you exceed the rate limit, you'll receive a `429 Too Many Requests` response.

## Versioning

The API version is included in the URL path. The current version is v1, which is implicit in the `/api/` prefix.

## Support

If you encounter any issues or have questions about the API, please contact:
- Email: [support@shinyleaves.io](mailto:support@shinyleaves.io)
