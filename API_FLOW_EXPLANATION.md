# Backend-Frontend API Flow Documentation

## Overview
This document explains how the FastAPI backend and React frontend are connected and communicate with each other.

---

## Architecture

### Backend (FastAPI - Python)
- **Location**: `main.py`
- **Port**: `http://localhost:8000`
- **Database**: PostgreSQL at `postgresql://postgres:2001@localhost:5432/products`
- **Framework**: FastAPI with SQLAlchemy ORM

### Frontend (React - JavaScript)
- **Location**: `frontend/src/`
- **Port**: `http://localhost:3000`
- **HTTP Client**: Axios

---

## CORS Configuration

The backend now has **CORS (Cross-Origin Resource Sharing)** middleware configured to allow requests from the frontend:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, PATCH, DELETE
    allow_headers=["*"],
)
```

**What this means**: 
- The frontend running on `localhost:3000` can make HTTP requests to the backend on `localhost:8000`
- All HTTP methods (GET, POST, PUT, PATCH, DELETE) are allowed
- This prevents CORS (Cross-Origin) errors

---

## API Endpoints

All endpoints are prefixed with `/products/` (note the trailing slash):

### 1. **GET /products/** - Fetch All Products
**Frontend call**:
```javascript
const res = await api.get("/products/");
```
**What happens**:
1. Frontend sends GET request to backend
2. Backend queries all products from PostgreSQL database
3. Returns array of product objects
4. Frontend displays them in a table

**Response Example**:
```json
[
  {
    "id": 1,
    "name": "Phone",
    "description": "A smartphone",
    "price": 699.99,
    "quantity": 50
  }
]
```

---

### 2. **GET /products/{id}** - Fetch Single Product
**Frontend call**:
```javascript
const res = await api.get("/products/1");
```
**What happens**:
1. Frontend sends GET request with product ID in the URL
2. Backend queries database for product with that ID
3. Returns single product object or error if not found

**Response Example**:
```json
{
  "id": 1,
  "name": "Phone",
  "description": "A smartphone",
  "price": 699.99,
  "quantity": 50
}
```

---

### 3. **POST /products/** - Create New Product
**Frontend call**:
```javascript
await api.post("/products/", {
  id: 5,
  name: "Keyboard",
  description: "Mechanical keyboard",
  price: 99.99,
  quantity: 25
});
```
**What happens**:
1. Frontend sends POST request with product data in request body
2. Backend receives the data and validates it using Pydantic `Product` model
3. Backend creates new record in PostgreSQL database
4. Returns the created product data
5. Frontend shows success message and refreshes product list

**Flow**:
```
User fills form → Clicks Submit → Frontend sends POST → Backend creates in DB → Response returned → Table updated
```

---

### 4. **PUT /products/{id}** - Replace Product (Full Update)
**Frontend call**:
```javascript
await api.put("/products/1", {
  id: 1,
  name: "Updated Phone",
  description: "Latest smartphone",
  price: 799.99,
  quantity: 45
});
```
**What happens**:
1. Frontend sends PUT request with product ID and complete product data
2. Backend finds product by ID
3. Backend replaces all fields with new data
4. Saves changes to PostgreSQL database
5. Returns success message

---

### 5. **PATCH /products/{id}** - Partial Update
**Frontend call**:
```javascript
await api.patch("/products/1", {
  name: "Updated Phone",
  price: 799.99
});
```
**Note**: Currently, the frontend uses PUT for updates, not PATCH

---

### 6. **DELETE /products/{id}** - Delete Product
**Frontend call**:
```javascript
await api.delete("/products/1");
```
**What happens**:
1. Frontend shows confirmation dialog: "Delete this product?"
2. If user confirms, sends DELETE request with product ID
3. Backend finds and deletes product from PostgreSQL database
4. Returns deleted product data in response
5. Frontend shows success message and refreshes table

**Flow**:
```
User clicks Delete → Confirmation dialog → Yes → Frontend sends DELETE → Backend deletes from DB → Table refreshes
```

---

## Complete Request-Response Flow Example

### Scenario: User Creates a New Product

```
STEP 1: User enters form data
┌─────────────────────────────────────────┐
│ Name: "Monitor"                         │
│ Description: "4K Display"               │
│ Price: 499.99                           │
│ Quantity: 15                            │
└─────────────────────────────────────────┘
            ↓
STEP 2: User clicks "Add Product" button
            ↓
STEP 3: Frontend (App.js) validates & sends POST request
┌─────────────────────────────────────────┐
│ POST http://localhost:8000/products/    │
│ Body: {                                 │
│   id: 5,                                │
│   name: "Monitor",                      │
│   description: "4K Display",            │
│   price: 499.99,                        │
│   quantity: 15                          │
│ }                                       │
└─────────────────────────────────────────┘
            ↓
STEP 4: Backend (main.py) receives request
        - Route handler: add_product()
        - Validates data using Pydantic model
        - Converts to SQLAlchemy Product model
        - Adds to database session
        - Commits to PostgreSQL
            ↓
STEP 5: Backend sends response back
┌─────────────────────────────────────────┐
│ HTTP 200 OK                             │
│ Body: {                                 │
│   id: 5,                                │
│   name: "Monitor",                      │
│   description: "4K Display",            │
│   price: 499.99,                        │
│   quantity: 15                          │
│ }                                       │
└─────────────────────────────────────────┘
            ↓
STEP 6: Frontend receives response
        - Shows: "Product created successfully"
        - Message auto-dismisses after 5 seconds
        - Calls fetchProducts() to refresh table
            ↓
STEP 7: Frontend fetches updated product list
        - Sends GET request to /products/
        - Backend returns all products from database
        - Frontend re-renders table with new product
```

---

## Data Models

### Frontend Model (JavaScript)
```javascript
// From models.js (Pydantic model used on backend)
const Product = {
  id: number,
  name: string,
  description: string,
  price: number,
  quantity: number
}
```

### Backend Model (Python)
```python
# From models.py (Pydantic model for validation)
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

# From database_models.py (SQLAlchemy ORM model)
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
```

---

## Axios Configuration

**File**: `frontend/src/App.js`

```javascript
const api = axios.create({
  baseURL: "http://localhost:8000",
});
```

This creates an Axios instance with:
- Base URL pointing to backend on port 8000
- All requests automatically get `http://localhost:8000` prepended
- Example: `api.get("/products/")` → `GET http://localhost:8000/products/`

---

## Error Handling

### Backend Error Response
If something goes wrong, backend returns error:
```json
{
  "detail": "Product not found"
}
```

### Frontend Error Handling
```javascript
try {
  const res = await api.get("/products/");
  setProducts(res.data);
} catch (err) {
  setError(err.response?.data?.detail || "Failed to fetch products");
}
```

---

## Database Connection Flow

```
Frontend Request
    ↓
FastAPI Route Handler
    ↓
Dependency Injection: get_db()
    ↓
SQLAlchemy Session
    ↓
PostgreSQL Connection
    ↓
Query/Insert/Update/Delete
    ↓
Commit/Rollback
    ↓
Session Closes
    ↓
Response to Frontend
```

---

## Key Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend Server | FastAPI | REST API framework |
| Database ORM | SQLAlchemy | Object-relational mapping |
| Database | PostgreSQL | Data persistence |
| Frontend Framework | React | UI rendering |
| HTTP Client | Axios | Making API requests |
| Middleware | CORS (Starlette) | Cross-origin request handling |

---

## Summary

**How it works**:
1. **Frontend** (React on port 3000) displays a table of products
2. **User interacts** with the UI (add, edit, delete, view products)
3. **Frontend makes API calls** using Axios to the backend
4. **Backend** (FastAPI on port 8000) receives requests
5. **Backend validates** data and interacts with PostgreSQL database
6. **Backend returns** JSON responses
7. **Frontend updates** the UI with the results
8. **CORS middleware** ensures the frontend can communicate with the backend

This architecture separates concerns: Frontend handles UI/UX, Backend handles business logic and data persistence.
