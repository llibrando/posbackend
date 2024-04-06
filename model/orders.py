# model/orders.py
from fastapi import Depends, HTTPException, APIRouter, Form
from model.db import get_db
import bcrypt
import mysql.connector
from pydantic import BaseModel
import time, datetime

class OrderUpdate(BaseModel):
    OrderStatus: str
    orderDate: str
    orderTime: str
    orderTotal: int

ordersRouter = APIRouter()
ordersRouter = APIRouter(tags=["orders"])

# CRUD operations

@ordersRouter.get("/orders/", response_model=list)
async def read_orders(
    db=Depends(get_db)
):
    query = "SELECT OrderID, OrderStatus,orderTime, orderTotal FROM orders"
    db[0].execute(query)
    orders = [{"OrderID": orders[0], "orderStatus": orders[1],"orderTime": orders[2],"orderTotal": orders[3]} for orders in db[0].fetchall()]
    return orders


@ordersRouter.get("/orders/{OrderID}", response_model=dict)
async def read_orders(
    OrderID: int, 
    db=Depends(get_db)
):
    query = "SELECT OrderID, orderStatus FROM orders WHERE OrderID = %s"
    db[0].execute(query, (OrderID,))
    orders = db[0].fetchone()
    if orders:                             
        return {
            "OrderID": orders[0],
            "orderStatus": orders[1],
        }
    raise HTTPException(status_code=404, detail="Order not found")

# -------------------PUT/UPDATE----------------------------------
@ordersRouter.post("/orders/", response_model=dict)
async def create_order(order_status: str, order_date: str, order_time: str, order_total: int, db=Depends(get_db)):
    try:
        # Insert the new order into the database
        query = "INSERT INTO orders (OrderStatus, orderDate, orderTime, orderTotal) VALUES (%s, %s, %s, %s)"
        db[0].execute(query, (order_status, order_date, order_time, order_total))
        db[1].commit()

        # Get the last inserted order ID
        order_id = db[0].lastrowid

        # Return success message
        return {"message": "Order created successfully", "order_id": order_id}
    except mysql.connector.Error as e:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
    finally:
        # Close the cursor and database connection
        db[0].close()

#update
@ordersRouter.put("/orders/{order_id}",response_model=dict)
async def update_order(order_id: int, order_update: OrderUpdate, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    # Prepare SQL query to update the order
    update_query = """
    UPDATE orders
    SET OrderStatus = %s, orderDate = %s, orderTime = %s, orderTotal = %s
    WHERE OrderID = %s
    """

    # Execute the SQL query with the provided data
    cursor = db.cursor()
    cursor.execute(update_query, (
        order_update.OrderStatus,
        order_update.orderDate,
        order_update.orderTime,
        order_update.orderTotal,
        order_id
    ))

    # Commit changes to the database
    db.commit()

    # Check if the update was successful
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "Order updated successfully"}

    # Code na gikan sa CASHIER na DELETE---------------------------------

@ordersRouter.delete("/orders/{order_id}", response_model=dict)
async def delete_order(
    order_id: int,
    db=Depends(get_db)
):
    # try:
        # Check if the cashier exists
        query_check_order = "SELECT OrderID FROM orders WHERE OrderID = %s"
        db[0].execute(query_check_order, (order_id,))
        existing_order = db[0].fetchone()

        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Delete the cashier
        query_delete_order = "DELETE FROM orders WHERE OrderID = %s"
        db[0].execute(query_delete_order, (order_id,))
        db[1].commit()

        return {"message": "Order deleted successfully"}