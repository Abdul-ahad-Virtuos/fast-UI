from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from db import session, engine
import database_models   
from sqlalchemy.orm import Session

products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),  
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

# Create tables first
database_models.Base.metadata.create_all(bind=engine)

# depedency injecion 
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close() 

def inti_db():
    db=session()

    count = db.query(database_models.Product).count()
    
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
         
        db.commit()
    db.close()

inti_db()


app = FastAPI()

# Add CORS middleware to allow requests from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def greet():
    return "yay !!"   


# @app.get("/products")
# def get_all_methods():

@app.get("/products/")
def get_all_products(db: Session = Depends(get_db)):
    # db = session()
    # db.query()
    db_products = db.query(database_models.Product).all()
    return db_products


# @app.get("/products/{id}")
# def get_products_with_id(id:int):
#     for product in products:
#         if product.id == id:
#             return product

@app.get("/products/{id}")
def get_products_with_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product

    return {"detail": "Product not found"}


# @app.post("/products/")
# def add_product(product : Product):
#     products.append(product)
#     return product 

@app.post("/products/")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product 




# @app.patch("/products/")
# def update_product (id:int , product : Product ,  db:Session = Depends(get_db)):
#     for i in range(len(products)):
#         if products[i].id == id :
#             products[i]=product
#             return "Added"
#         
#     return "No Product added "

@app.patch("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return {"message": "Product updated", "product": product}
    return {"message": "Product not found"}


# @app.put("/products/")
# def update_product_put(product: Product):
#     for i in range(len(products)):
#         if products[i].id == product.id:
#             products[i] = product
#             return {"message": "Product updated", "product": product.__dict__}
#     
#     return {"message": "Product not found"}

@app.put("/products/{id}")
def update_product_put(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return {"message": "Product updated", "product": product}
    return {"message": "Product not found"}


# @app.delete("/products/{id}")
# def delete_product(id:int):
#     for i in range(len(products)) :
#         if products[i].id == id :
#             product_data = products[i].__dict__
#             del products[i]
#             return {"message" : "product deleted", "product" : product_data}
#     
#     return "no product with this id"

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        product_data = {
            "id": db_product.id,
            "name": db_product.name,
            "description": db_product.description,
            "price": db_product.price,
            "quantity": db_product.quantity
        }
        db.delete(db_product)
        db.commit()
        return {"message": "product deleted", "product": product_data}
    return {"message": "no product with this id"}
