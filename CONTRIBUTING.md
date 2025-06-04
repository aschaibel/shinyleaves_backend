# Contributing to ShinyLeaves Backend

Thank you for your interest in contributing to the ShinyLeaves backend project! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Documentation Guidelines](#documentation-guidelines)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)
- [Communication](#communication)

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up your development environment (see [Development Environment Setup](#development-environment-setup))
4. Create a new branch for your feature or bug fix
5. Make your changes
6. Run tests to ensure your changes don't break existing functionality
7. Commit your changes
8. Push to your fork
9. Submit a pull request

## Development Environment Setup

Follow the setup instructions in the [README.md](README.md) file to set up your development environment.

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

## Project Structure

The project follows a layered architecture pattern as described in the [architecture documentation](docs/architecture.md). The main components are:

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

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style
- Use 4 spaces for indentation (not tabs)
- Maximum line length of 88 characters (following Black's default)
- Use meaningful variable and function names
- Add docstrings to all functions, classes, and modules

### Type Hints

- Use type hints for function parameters and return values
- Use Optional[] for parameters that can be None

### Error Handling

- Use appropriate exception handling
- Raise specific exceptions rather than generic ones
- Document exceptions in function docstrings

## Testing Guidelines

- Write tests for all new features and bug fixes
- Ensure all tests pass before submitting a pull request
- Follow the existing test structure in the `tests/` directory
- Use pytest fixtures for common test setup
- Include both positive and negative test cases
- Test edge cases

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app
```

## Commit Guidelines

- Use clear and descriptive commit messages
- Start the commit message with a verb in the present tense (e.g., "Add", "Fix", "Update")
- Reference issue numbers in commit messages when applicable
- Keep commits focused on a single change
- Make frequent, smaller commits rather than infrequent, large commits

## Pull Request Process

1. Ensure your code follows the project's coding standards
2. Update documentation if necessary
3. Add or update tests as needed
4. Ensure all tests pass
5. Submit a pull request to the `main` branch
6. Wait for code review and address any feedback

## Documentation Guidelines

- Update documentation for any changes to the API, architecture, or functionality
- Follow the existing documentation style
- Use clear and concise language
- Include code examples where appropriate
- Document all public functions, classes, and modules with docstrings

## Issue Reporting

When reporting issues, please include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots or error messages (if applicable)
- Environment information (OS, browser, etc.)

## Feature Requests

When requesting new features, please include:

- A clear and descriptive title
- A detailed description of the feature
- Why the feature would be beneficial
- Any potential implementation details

## Communication

- For questions or discussions, please use the GitHub Discussions feature
- For bug reports or feature requests, please use GitHub Issues
- For more immediate communication, contact us at [support@shinyleaves.io](mailto:support@shinyleaves.io)

Thank you for contributing to ShinyLeaves!