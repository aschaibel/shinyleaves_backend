# ShinyLeaves Database Schema Documentation

This document provides an overview of the database schema used in the ShinyLeaves application. It includes information about tables, their relationships, and field descriptions.

## Tables Overview

The ShinyLeaves database consists of the following main tables:

- **Product**: Stores information about products, including weed-related attributes
- **Order**: Stores information about customer orders
- **Customer**: Stores information about customers

## Entity Relationship Diagram

```
+-------------+       +-------------+       +-------------+
|   Product   |       |   Order     |       |  Customer   |
+-------------+       +-------------+       +-------------+
| p_id (PK)   |       | o_id (PK)   |       | c_id (PK)   |
| name        |       | p_id (FK)   |----+  | name        |
| price       |       | amount      |    |  | email       |
| genetic     |       | order_nr    |    |  | password    |
| thc         |       +-------------+    |  | address     |
| cbd         |                          |  +-------------+
| effect      |                          |
| slug        |                          |
+-------------+                          |
                                         |
                                         |
                                +-------------+
                                |   Product   |
                                +-------------+
                                | p_id (PK)   |
                                | name        |
                                | price       |
                                | genetic     |
                                | thc         |
                                | cbd         |
                                | effect      |
                                | slug        |
                                +-------------+
```

## Table Descriptions

### Product

The Product table stores information about products available in the store, including weed-related attributes.

| Column | Type | Description | Constraints |
|--------|------|-------------|------------|
| p_id | Integer | Unique identifier for the product | Primary Key, Auto-increment |
| name | String(255) | Name of the product | Not Null |
| price | Float | Price of the product | Not Null |
| genetic | String(255) | Genetic information of the weed | Not Null |
| thc | Float | THC content of the weed | Not Null |
| cbd | Float | CBD content of the weed | Not Null |
| effect | String(255) | Effect of the weed | Not Null |
| slug | String(255) | Path to the product picture | Nullable |

### Order

The Order table stores information about customer orders.

| Column | Type | Description | Constraints |
|--------|------|-------------|------------|
| o_id | Integer | Unique identifier for the order | Primary Key, Auto-increment |
| p_id | Integer | Foreign key to the Product table | Foreign Key, Not Null |
| c_id | Integer | Foreign key to the Customer table | Foreign Key, Not Null |
| amount | Integer | Amount of the product ordered | Not Null |
| order_nr | VARCHAR | Order number for reference | Not Null |

### Customer

The Customer table stores information about customers.

| Column | Type | Description | Constraints |
|--------|------|-------------|------------|
| c_id | Integer | Unique identifier for the customer | Primary Key, Auto-increment |
| name | String(255) | Name of the customer | Not Null |
| email | String(255) | Email of the customer | Not Null, Unique |
| password | String(255) | Hashed password of the customer | Not Null |
| address | String(255) | Address of the customer | Nullable |

## Relationships

1. **Order to Product**: Many-to-One
   - An order contains one product (in a specific amount)
   - A product can be in multiple orders

2. **Order to Customer**: Many-to-One
   - An order belongs to one customer
   - A customer can have multiple orders

## Indexes

- Primary keys on all tables (p_id, o_id, c_id)
- Foreign key indexes (p_id and c_id in Order)
- Email index in Customer table for quick lookups

## Notes

- The database schema is created automatically when the application starts using SQLAlchemy's `create_all` method.
- Foreign key constraints ensure data integrity between related tables.
- The schema may evolve over time as new features are added to the application.
