# Ecommerce FastAPI Backend

A professional FastAPI-based ecommerce backend with MongoDB integration.

## Features

- **Product Management**: Create and list products with sizes and pricing
- **Order Management**: Create orders and retrieve user order history
- **Advanced Filtering**: Search products by name and filter by size
- **Pagination**: Efficient pagination for all list endpoints
- **Data Validation**: Comprehensive Pydantic schema validation
- **Error Handling**: Professional error handling and logging
- **MongoDB Integration**: Async MongoDB operations with Motor

## API Endpoints

### Products

- `POST /products` - Create a new product
- `GET /products` - List products with filtering and pagination

### Orders

- `POST /orders` - Create a new order
- `GET /orders/{user_id}` - Get user's order history

## Project Structure

```
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                   # Environment configuration
└── app/
    ├── __init__.py
    ├── database/
    │   └── connection.py   # MongoDB connection management
    ├── models/            # Database models (future use)
    ├── routes/
    │   ├── products.py    # Product API endpoints
    │   └── orders.py      # Order API endpoints
    ├── schemas/
    │   └── schemas.py     # Pydantic schemas for validation
    └── services/
        ├── product_service.py  # Product business logic
        └── order_service.py    # Order business logic
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup MongoDB

- **Local MongoDB**: Install MongoDB locally and ensure it's running on port 27017
- **MongoDB Atlas**: Update the `MONGODB_URL` in `.env` with your Atlas connection string

### 3. Configure Environment

Update `.env` file with your MongoDB connection details:

```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ecommerce_db
```

### 4. Run the Application

```bash
python main.py
```
`
**Note**: The application will automatically connect to MongoDB on startup. Ensure MongoDB is running and accessible before starting the application.

The API will be available at `http://localhost:8000`



## API Usage Examples

### Create a Product

```bash
POST http://localhost:8000/products
Content-Type: application/json

{
  "name": "T-Shirt",
  "price": 29.99,
  "sizes": [
    {"size": "S", "quantity": 10},
    {"size": "M", "quantity": 15},
    {"size": "L", "quantity": 8}
  ]
}
```

### List Products

```bash
GET http://localhost:8000/products?name=shirt&size=M&limit=10&offset=0
```

### Create an Order

```bash
POST http://localhost:8000/orders
Content-Type: application/json

{
  "userId": "user_123",
  "items": [
    {"productId": "product_id_here", "qty": 2}
  ]
}
```

### Get User Orders

```bash
GET http://localhost:8000/orders/user_123?limit=10&offset=0
```

## Testing with Postman

1. Import the API into Postman using the OpenAPI URL: `http://localhost:8000/openapi.json`
2. Set base URL to `http://localhost:8000`
3. Test all endpoints with the example payloads above

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for flexible data storage
- **Motor**: Async MongoDB driver for Python
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running the application
