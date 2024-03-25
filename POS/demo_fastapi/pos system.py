from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
class Product(BaseModel):
    name: str
    price: float
    quantity: int

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    items: List[OrderItem]

@app.get("/products/")
async def get_products():
    return products_db

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    for product in products_db:
        if product['id'] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/orders/")
async def create_order(order: Order):
    total_price = 0
    for item in order.items:
        product_id = item.product_id
        quantity = item.quantity
        for product in products_db:
            if product['id'] == product_id:
                if product['quantity'] < quantity:
                    raise HTTPException(status_code=400, detail="Insufficient stock")
                total_price += product['price'] * quantity
                product['quantity'] -= quantity
                break
        else:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

    return {"message": "Order placed successfully", "total_price": total_price}

@app.post("/products/")
async def add_product(product: Product):
    products_db.append(product.dict())
    return {"message": "Product added successfully"}

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    for p in products_db:
        if p['id'] == product_id:
            p.update(product.dict())
            return {"message": "Product updated successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    for i, product in enumerate(products_db):
        if product['id'] == product_id:
            del products_db[i]
            return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")