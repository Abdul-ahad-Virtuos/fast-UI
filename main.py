from fastapi import FastAPI
from models import Product
from db import session 

products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

app = FastAPI()

@app.get("/")
async def greet():
    return "yay !!"   


# @app.get("/products")
# def get_all_methods():

@app.get("/product")
def get_all_products():
    db = session()
    # query
    db.query()
    return products


@app.get("/product/{id}")
def get_products_with_id(id:int):
    for product in products:
        if product.id == id:
            return product

    return "no products for the id"


@app.post("/add_product")
def add_product(product : Product):
    products.append(product)
    

@app.patch("/update_product")
def update_product (id:int , product : Product):
    for i in range(len(products)):
        if products[i].id == id :
            products[i]=product
            return "Added"
        
    return "No Product added "


@app.put("/product")
def update_product_put(product: Product):
    for i in range(len(products)):
        if products[i].id == product.id:
            products[i] = product
            return {"message": "Product updated", "product": product.__dict__}
    
    return {"message": "Product not found"}


@app.delete("/product/{id}")
def delete_product(id:int):
    for i in range(len(products)) :
        if products[i].id == id :
            product_data = products[i].__dict__
            del products[i]
            return {"message" : "product deleted", "product" : product_data}
    
    return "no product with this id"
