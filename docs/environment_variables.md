# ShinyLeaves Environment Variables Documentation

This document provides information about the environment variables used by the ShinyLeaves application and how to configure them.

## Environment Variables Overview

Environment variables are used to configure the application without changing the code. They allow for different configurations in different environments (development, testing, production).

## Required Environment Variables

The following environment variables are required for the application to function properly:

### Database Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `DATABASE_URL` | Database connection string | `mysql+pymysql://root:password@db:3306/shinyleaves` | `mysql+pymysql://user:password@localhost:3306/shinyleaves` |

### Authentication

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `SECRET_KEY` | Secret key for JWT token generation | None (must be provided) | `your-secret-key-here` |
| `ALGORITHM` | Algorithm used for JWT token generation | `HS256` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time in minutes | `30` | `60` |

## Optional Environment Variables

The following environment variables are optional and have default values:

### API Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `API_PREFIX` | Prefix for all API endpoints | `/api` | `/api/v1` |
| `DEBUG` | Enable debug mode | `False` | `True` |
| `CORS_ORIGINS` | Allowed origins for CORS | `["*"]` | `["http://localhost:4200", "https://example.com"]` |

### Server Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `HOST` | Host to bind the server to | `0.0.0.0` | `127.0.0.1` |
| `PORT` | Port to bind the server to | `8000` | `5000` |

## Environment Variables in Different Environments

### Development

For development, you can set environment variables in a `.env` file in the root directory of the project:

```
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/shinyleaves
SECRET_KEY=dev-secret-key
DEBUG=True
```

### Docker

When using Docker, you can set environment variables in the `docker-compose.yml` file:

```yaml
services:
  backend:
    build: .
    environment:
      - DATABASE_URL=mysql+pymysql://root:password@db:3306/shinyleaves
      - SECRET_KEY=docker-secret-key
      - DEBUG=False
```

### Production

In production, you should set environment variables using the appropriate method for your deployment platform:

- **Kubernetes**: Use ConfigMaps and Secrets
- **AWS**: Use AWS Parameter Store or Secrets Manager
- **Heroku**: Use Heroku Config Vars
- **Azure**: Use Azure App Configuration or Key Vault

## Security Considerations

- Never commit sensitive environment variables (like `SECRET_KEY`) to version control
- Use different secret keys for different environments
- Consider using a secrets management service for production environments
- Rotate secrets periodically

## Troubleshooting

If the application fails to start or behaves unexpectedly, check that all required environment variables are set correctly.

Common issues:
- Missing required environment variables
- Incorrect database connection string
- Invalid secret key format
- Incorrect permissions for database user

## Example Configuration

Here's an example of a complete environment configuration for development:

```
# Database
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/shinyleaves

# Authentication
SECRET_KEY=dev-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# API
API_PREFIX=/api
DEBUG=True
CORS_ORIGINS=["http://localhost:4200"]

# Server
HOST=0.0.0.0
PORT=8000
```