# Quick Reference: Backend-Frontend Communication

## 🚀 Quick Start

### Terminal 1: Start Backend
```bash
uvicorn main:app --reload
```
✅ Backend runs on: `http://localhost:8000`

### Terminal 2: Start Frontend
```bash
cd frontend
npm start
```
✅ Frontend runs on: `http://localhost:3000`

---

## 📋 API Endpoints Summary

### Get Products
```javascript
// Fetch all products
GET /products/
// Response: Array of products

// Fetch single product
GET /products/1
// Response: Single product object
```

### Create Product
```javascript
// Add new product
POST /products/
// Body: { id, name, description, price, quantity }
// Response: Created product
```

### Update Product
```javascript
// Update product (replace all fields)
PUT /products/1
// Body: { id, name, description, price, quantity }
// Response: { message, product }

// Update product (partial update)
PATCH /products/1
// Body: { name, price } // Only changed fields
// Response: { message, product }
```

### Delete Product
```javascript
// Delete product
DELETE /products/1
// Response: { message, product: deleted_product_data }
```

---

## 🔒 CORS is Enabled ✅

Frontend on `localhost:3000` can make requests to backend on `localhost:8000`

```python
# This is already configured in main.py:
CORSMiddleware(
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Data Flow

```
User Action (Frontend)
    ↓
Axios API Call
    ↓
FastAPI Route Handler
    ↓
SQLAlchemy ORM Query
    ↓
PostgreSQL Database
    ↓
Response JSON
    ↓
React State Update
    ↓
UI Re-render
```

---

## 🐛 Testing Endpoints

### Using curl
```bash
# Get all
curl http://localhost:8000/products/

# Get one
curl http://localhost:8000/products/1

# Create
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"id":5,"name":"Monitor","description":"4K","price":499.99,"quantity":10}'

# Update
curl -X PUT http://localhost:8000/products/1 \
  -H "Content-Type: application/json" \
  -d '{"id":1,"name":"Updated","description":"New","price":799.99,"quantity":40}'

# Delete
curl -X DELETE http://localhost:8000/products/1
```

---

## ✅ What Was Fixed

1. ✅ **CORS Middleware** - Frontend can now communicate with backend
2. ✅ **Endpoint Naming** - Changed `/product/` to `/products/`
3. ✅ **Type Hints** - Improved Python formatting
4. ✅ **Error Handling** - Consistent JSON responses
5. ✅ **Dependencies** - Added python-multipart to requirements.txt

---

## 📁 Files Modified

- `main.py` - CORS + endpoint fixes
- `requirements.txt` - Added python-multipart
- `API_FLOW_EXPLANATION.md` - Full documentation (NEW)
- `CHANGES_SUMMARY.md` - Detailed changes (NEW)

---

## 🔧 Troubleshooting

### Issue: CORS Error in Console
**Solution**: Make sure backend is running with CORS middleware loaded
```bash
uvicorn main:app --reload
```

### Issue: 404 Not Found
**Solution**: Check endpoint path matches - should be `/products/` not `/product/`

### Issue: Database Connection Error
**Solution**: Ensure PostgreSQL is running and connection string is correct:
```
postgresql://postgres:2001@localhost:5432/products
```

### Issue: Module Not Found
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

---

## 📚 Related Documentation

- [API_FLOW_EXPLANATION.md](./API_FLOW_EXPLANATION.md) - Complete flow documentation
- [CHANGES_SUMMARY.md](./CHANGES_SUMMARY.md) - Detailed change list
- FastAPI Docs: `http://localhost:8000/docs` (interactive)
- FastAPI ReDoc: `http://localhost:8000/redoc` (alternative docs)

---

**Status**: ✅ Backend & Frontend ready to communicate!
