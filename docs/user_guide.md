# ShinyLeaves API User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
   - [Installation](#installation)
   - [Environment Setup](#environment-setup)
3. [Authentication](#authentication)
   - [Registration](#registration)
   - [Login](#login)
   - [Using Authentication Tokens](#using-authentication-tokens)
4. [API Endpoints](#api-endpoints)
   - [Products](#products)
   - [Orders](#orders)
   - [Customer Account](#customer-account)
5. [Common Use Cases](#common-use-cases)
   - [Browsing Products](#browsing-products)
   - [Placing an Order](#placing-an-order)
   - [Viewing Order History](#viewing-order-history)
6. [Troubleshooting](#troubleshooting)
   - [Common Errors](#common-errors)
   - [Support](#support)

## Introduction

Welcome to the ShinyLeaves API User Guide. This document provides comprehensive information on how to use the ShinyLeaves API to interact with our online cannabis store platform. The API allows you to browse products, place orders, and manage your customer account.

ShinyLeaves is a modern, secure, and user-friendly online cannabis store. Designed with style and simplicity in mind, it allows users to browse premium strains, shop accessories, and enjoy a seamless checkout experience — all from the comfort of home.

## Getting Started

### Installation

To use the ShinyLeaves API, you don't need to install anything on your system. The API is accessible via HTTP requests to our server. However, if you want to run the API locally for development or testing purposes, follow these steps:

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

### Environment Setup

The application uses the following environment variables:

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for JWT token generation
- `ALGORITHM`: Algorithm used for JWT token generation (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes

## Authentication

The ShinyLeaves API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints, you need to obtain an access token by registering and logging in.

### Registration

To create a new customer account, send a POST request to the `/api/register` endpoint:

```
POST /api/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "address": "123 Main St, City"
}
```

If successful, you'll receive a response with status code 201 and the created customer data:

```json
{
    "c_id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "address": "123 Main St, City"
}
```

### Login

To log in and obtain an access token, send a POST request to the `/api/login` endpoint:

```
POST /api/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

If successful, you'll receive a response with status code 200 and the access token:

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### Using Authentication Tokens

To access protected endpoints, include the access token in the Authorization header of your requests:

```
GET /api/orders/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

The access token is valid for 30 minutes. After it expires, you need to log in again to obtain a new token.

## API Endpoints

### Products

#### Get Products

Retrieve a list of products with pagination:

```
GET /api/products/?skip=0&limit=10
```

Parameters:
- `skip` (optional): Number of products to skip (default: 0)
- `limit` (optional): Maximum number of products to return (default: 10)

Response (200 OK):
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

#### Get Product by ID

Retrieve a specific product by its ID:

```
GET /api/products/1
```

Response (200 OK):
```json
{
    "p_id": 1,
    "name": "Premium Indica",
    "price": 29.99,
    "genetic": "Indica",
    "thc": 18.5,
    "cbd": 0.2,
    "effect": "Relaxing",
    "slug": "premium-indica"
}
```

#### Create Products (Admin Only)

Create multiple products (requires admin privileges):

```
POST /api/products/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

[
    {
        "name": "New Hybrid Strain",
        "price": 27.99,
        "genetic": "Hybrid",
        "thc": 20.0,
        "cbd": 0.5,
        "effect": "Balanced",
        "slug": "new-hybrid-strain"
    },
    {
        "name": "CBD Special",
        "price": 32.99,
        "genetic": "Indica",
        "thc": 5.0,
        "cbd": 15.0,
        "effect": "Therapeutic",
        "slug": "cbd-special"
    }
]
```

Response (201 Created):
```json
[
    {
        "p_id": 3,
        "name": "New Hybrid Strain",
        "price": 27.99,
        "genetic": "Hybrid",
        "thc": 20.0,
        "cbd": 0.5,
        "effect": "Balanced",
        "slug": "new-hybrid-strain"
    },
    {
        "p_id": 4,
        "name": "CBD Special",
        "price": 32.99,
        "genetic": "Indica",
        "thc": 5.0,
        "cbd": 15.0,
        "effect": "Therapeutic",
        "slug": "cbd-special"
    }
]
```

#### Update Product (Admin Only)

Update a product (requires admin privileges):

```
PATCH /api/products/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "price": 31.99,
    "thc": 19.0
}
```

Response (200 OK):
```json
{
    "p_id": 1,
    "name": "Premium Indica",
    "price": 31.99,
    "genetic": "Indica",
    "thc": 19.0,
    "cbd": 0.2,
    "effect": "Relaxing",
    "slug": "premium-indica"
}
```

#### Delete Product (Admin Only)

Delete a product (requires admin privileges):

```
DELETE /api/products/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Response (204 No Content)

### Orders

#### Create Order

Create a new order (requires authentication):

```
POST /api/order/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "customer_id": 1,
    "product_id": 2,
    "quantity": 3,
    "total_price": 74.97
}
```

Response (200 OK):
```json
{
    "o_id": "ORD123",
    "customer_id": 1,
    "product_id": 2,
    "quantity": 3,
    "total_price": 74.97
}
```

#### Get Orders

Retrieve a list of orders with pagination (requires authentication):

```
GET /api/orders/?skip=0&limit=10
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Parameters:
- `skip` (optional): Number of orders to skip (default: 0)
- `limit` (optional): Maximum number of orders to return (default: 10)

Response (200 OK):
```json
[
    {
        "o_id": "ORD123",
        "customer_id": 1,
        "product_id": 2,
        "quantity": 3,
        "total_price": 74.97
    }
]
```

#### Get Order by ID

Retrieve a specific order by its ID (requires authentication):

```
GET /api/orders/ORD123
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Response (200 OK):
```json
{
    "o_id": "ORD123",
    "customer_id": 1,
    "product_id": 2,
    "quantity": 3,
    "total_price": 74.97
}
```

### Customer Account

#### Get Customer Profile (Admin Only)

Retrieve a specific customer by ID (requires admin privileges):

```
GET /api/customers/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Response (200 OK):
```json
{
    "c_id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "address": "123 Main St, City"
}
```

#### Get All Customers (Admin Only)

Retrieve a list of customers with pagination (requires admin privileges):

```
GET /api/customers/?skip=0&limit=10
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Parameters:
- `skip` (optional): Number of customers to skip (default: 0)
- `limit` (optional): Maximum number of customers to return (default: 10)

Response (200 OK):
```json
[
    {
        "c_id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+1234567890",
        "address": "123 Main St, City"
    }
]
```

## Common Use Cases

### Browsing Products

To browse products, you can use the `/api/products/` endpoint. You can paginate through the results by using the `skip` and `limit` parameters:

```
GET /api/products/?skip=0&limit=10
```

For the next page:

```
GET /api/products/?skip=10&limit=10
```

### Placing an Order

To place an order, follow these steps:

1. **Register or log in to get an access token**
   ```
   POST /api/login
   Content-Type: application/json

   {
       "email": "user@example.com",
       "password": "securepassword123"
   }
   ```

2. **Create an order using the access token**
   ```
   POST /api/order/
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   Content-Type: application/json

   {
       "customer_id": 1,
       "product_id": 2,
       "quantity": 3,
       "total_price": 74.97
   }
   ```

### Viewing Order History

To view your order history, use the `/api/orders/` endpoint with your access token:

```
GET /api/orders/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Troubleshooting

### Common Errors

#### 401 Unauthorized

This error occurs when you try to access a protected endpoint without a valid access token. Make sure you've included the token in the Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

If you've included the token and still get this error, your token might have expired. Try logging in again to get a new token.

#### 403 Forbidden

This error occurs when you try to access an admin-only endpoint without admin privileges. Only users with admin privileges can access these endpoints.

#### 404 Not Found

This error occurs when the requested resource doesn't exist. Check that you're using the correct ID in your request.

#### 400 Bad Request

This error occurs when your request is malformed or contains invalid data. Check the error message for details on what went wrong.

### Support

If you encounter any issues or have questions about using the ShinyLeaves API, please contact our support team:

- Email: support@shinyleaves.io
- Website: https://shinyleaves.io
- Twitter: @shinyleaves

---

*ShinyLeaves — Elevate your experience.*
