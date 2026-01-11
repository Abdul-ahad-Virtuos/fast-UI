# System Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    BROWSER                                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │         React Frontend (localhost:3000)                   │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │ App.js                                              │  │  │
│  │  │ - State Management (products, form, messages)       │  │  │
│  │  │ - Event Handlers (add, edit, delete)                │  │  │
│  │  │ - Axios HTTP Client                                 │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────┬───────────────────────────────────────┘  │
└────────────────────┼──────────────────────────────────────────┘
                     │
                     │ HTTP Requests/Responses
                     │ (CORS Enabled ✅)
                     │
         ┌───────────▼───────────────┐
         │  NETWORK (localhost)      │
         │  Port 8000 ← Port 3000    │
         └───────────┬───────────────┘
                     │
┌────────────────────▼──────────────────────────────────────────┐
│              FastAPI Backend (localhost:8000)                  │
│  ┌───────────────────────────────────────────────────────────┐│
│  │ CORS Middleware                                            ││
│  │ - Allows localhost:3000                                    ││
│  │ - Allows all HTTP methods                                  ││
│  └───────────────────────────────────────────────────────────┘│
│  ┌───────────────────────────────────────────────────────────┐│
│  │ Route Handlers (main.py)                                   ││
│  │                                                            ││
│  │ GET  /products/       → get_all_products()                ││
│  │ GET  /products/{id}   → get_products_with_id()            ││
│  │ POST /products/       → add_product()                     ││
│  │ PUT  /products/{id}   → update_product_put()              ││
│  │ PATCH/products/{id}   → update_product()                  ││
│  │ DELETE /products/{id} → delete_product()                  ││
│  └────────────────┬──────────────────────────────────────────┘│
└────────────────┼───────────────────────────────────────────────┘
                 │
                 │ Queries/Commands
                 │ (SQLAlchemy ORM)
                 │
         ┌───────▼────────────┐
         │ SQLAlchemy ORM     │
         │ (database_models)  │
         │                    │
         │ Product Model:     │
         │ - id               │
         │ - name             │
         │ - description      │
         │ - price            │
         │ - quantity         │
         └───────┬────────────┘
                 │
                 │ SQL Queries
                 │
         ┌───────▼────────────────────────────┐
         │  PostgreSQL Database               │
         │  Connection:                        │
         │  postgresql://postgres:2001@       │
         │  localhost:5432/products           │
         │                                    │
         │  Table: products                   │
         │  - Stores all product records      │
         │  - Persists data                   │
         └────────────────────────────────────┘
```

---

## Request-Response Flow Diagram

### Example: User Creates a Product

```
┌──────────────────────────────────────────────────────────────────┐
│ FRONTEND (React)                                                  │
│ User fills form: name="Phone", price=699.99                      │
│ Clicks "Add Product" button                                       │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         │ 1. handleSubmit() triggered
                         │
         ┌───────────────▼────────────────────┐
         │ Validate form data                 │
         │ Convert types (string → number)    │
         └───────────────┬────────────────────┘
                         │
                         │ 2. Call api.post()
                         │    (Axios HTTP request)
                         │
         ┌───────────────▼────────────────────┐
         │ POST /products/                    │
         │ Content-Type: application/json     │
         │                                    │
         │ {                                  │
         │   "id": 5,                         │
         │   "name": "Phone",                 │
         │   "price": 699.99,                 │
         │   "quantity": 50                   │
         │ }                                  │
         └───────────────┬────────────────────┘
                         │
                         │ NETWORK
                         │ HTTP Request
                         │
         ┌───────────────▼────────────────────┐
         │ CORS Middleware (Starlette)        │
         │ Check: Origin = localhost:3000? ✅ │
         │ Check: Method = POST? ✅           │
         │ Allow request to proceed           │
         └───────────────┬────────────────────┘
                         │
         ┌───────────────▼────────────────────┐
         │ FastAPI Route Handler              │
         │ add_product() called                │
         │                                    │
         │ 1. Receive JSON body               │
         │ 2. Validate with Pydantic model    │
         │    (Product schema)                │
         │ 3. Convert to SQLAlchemy model     │
         └───────────────┬────────────────────┘
                         │
         ┌───────────────▼────────────────────┐
         │ Database Operation                 │
         │                                    │
         │ db.add(product_record)             │
         │ db.commit()                        │
         │                                    │
         │ INSERT INTO products (...) VALUES  │
         │ COMMIT;                            │
         └───────────────┬────────────────────┘
                         │
         ┌───────────────▼────────────────────┐
         │ Database Confirms                  │
         │ Row inserted with id=5             │
         │ Transaction committed              │
         └───────────────┬────────────────────┘
                         │
         ┌───────────────▼────────────────────┐
         │ Backend Response (JSON)            │
         │                                    │
         │ HTTP 200 OK                        │
         │                                    │
         │ {                                  │
         │   "id": 5,                         │
         │   "name": "Phone",                 │
         │   "price": 699.99,                 │
         │   "quantity": 50                   │
         │ }                                  │
         └───────────────┬────────────────────┘
                         │
                         │ NETWORK
                         │ HTTP Response
                         │
         ┌───────────────▼────────────────────┐
         │ FRONTEND (React)                   │
         │ Response received                  │
         │                                    │
         │ 1. data = response.data            │
         │ 2. setMessage("Product created")   │
         │ 3. resetForm()                     │
         └───────────────┬────────────────────┘
                         │
         ┌───────────────▼────────────────────┐
         │ Refresh Product List               │
         │                                    │
         │ Call: fetchProducts()              │
         │ GET /products/                     │
         │                                    │
         │ Response: [product1, product2,     │
         │           product3, ..., product5] │
         └───────────────┬────────────────────┘
                         │
         ┌───────────────▼────────────────────┐
         │ Update React State                 │
         │                                    │
         │ setProducts(response.data)         │
         │ Component re-renders with new list │
         └───────────────┬────────────────────┘
                         │
         ┌───────────────▼────────────────────┐
         │ User Sees                          │
         │ ✅ Success message                 │
         │ ✅ New product in table            │
         │ ✅ Form cleared                    │
         └───────────────────────────────────┘
```

---

## Component Interaction Diagram

```
┌────────────────────┐
│   React Component   │
│   (App.js)         │
└──────────┬─────────┘
           │
           ├─ State: products, form, loading, error, message
           │
           ├─ Effects: fetch on mount, auto-dismiss messages
           │
           ├─ Handlers: 
           │  ├─ fetchProducts()
           │  ├─ handleSubmit()
           │  ├─ handleEdit()
           │  ├─ handleDelete()
           │  └─ handleChange()
           │
           └─ Renders: Table, Form, Messages
                  │
                  └─ Uses Axios Client
                     │
                     └─ Makes HTTP Requests
                        │
                        └─ FastAPI Backend
                           │
                           ├─ Route: GET /products/
                           ├─ Route: POST /products/
                           ├─ Route: PUT /products/{id}
                           ├─ Route: DELETE /products/{id}
                           │
                           └─ Database Operations
                              │
                              └─ PostgreSQL Table
```

---

## Data Type Flow

```
Frontend JavaScript Type
    │
    ├─ String: name, description
    ├─ Number: id, price, quantity
    │
    └─ Axios serializes to JSON
       │
       ├─ HTTP POST body (application/json)
       │
       └─ Backend receives JSON
          │
          ├─ Pydantic validates & converts
          │  ├─ "5" → 5 (string to int)
          │  ├─ "699.99" → 699.99 (string to float)
          │
          └─ SQLAlchemy ORM model
             │
             ├─ Python types
             │  ├─ Integer: id, quantity
             │  ├─ String: name, description
             │  ├─ Float: price
             │
             └─ Database column types
                ├─ INT: id, quantity
                ├─ VARCHAR: name, description
                ├─ FLOAT: price
```

---

## Error Handling Flow

```
Frontend Error Scenario
│
├─ Network Error
│  └─ catch (err) → setError("Failed to fetch...")
│
├─ Validation Error (400)
│  └─ err.response.data.detail → Display error message
│
├─ Server Error (500)
│  └─ catch (err) → Generic error message
│
└─ Success
   └─ Show success message (5 second timeout)
```

---

## CORS Flow

```
Browser (localhost:3000) makes request to Backend (localhost:8000)

Browser sends:
┌─────────────────────────────┐
│ Origin: http://localhost:3000│  ← Browser adds this header
│ GET /products/ HTTP/1.1      │
└─────────────────────────────┘
                │
                ├─ CORS Preflight (for complex requests)
                │  OPTIONS /products/ 
                │  → Middleware checks origin
                │  → Sends back allowed methods
                │
                └─ Actual Request
                   POST /products/
                   → Middleware checks origin ✅
                   → Origin matches config ✅
                   → Allow request to proceed ✅
                   → Return response with CORS headers

Response includes:
┌────────────────────────────────────────┐
│ Access-Control-Allow-Origin:           │
│   http://localhost:3000 ✅              │
│ Access-Control-Allow-Methods: * ✅      │
│ Access-Control-Allow-Headers: * ✅      │
└────────────────────────────────────────┘

Browser receives response → No CORS error ✅
```

---

This completes the architecture documentation!
