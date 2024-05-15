# model/orders.py
from fastapi import Depends, HTTPException, APIRouter, Form
from model.db import get_db
import mysql.connector
from pydantic import BaseModel
from datetime import datetime, timedelta

ordersRouter = APIRouter(tags=["Orders"])

# CRUD operations

@ordersRouter.get("/orders/showOrders", response_model=list)
async def read_orders(db=Depends(get_db)):  
    query = "SELECT * FROM orders WHERE orderType IN ('Cash', 'Gcash')"
    db[0].execute(query)
    orders = [{
        "OrderID": order[0],
        "orderItem": order[1],
        "orderType": order[2],
        "orderDate": order[3],
        "orderTime": str(timedelta(seconds=order[4].seconds)),  # Convert time duration to string
        "orderTotal": order[5]
    } for order in db[0].fetchall()]
    return orders

@ordersRouter.get("/orders/payment-types", response_model=list)
async def get_payment_types(db=Depends(get_db)):
    try:
        # Query to get payment type data
        query = "SELECT orderType, COUNT(*), SUM(orderTotal) FROM orders GROUP BY orderType"

        db[0].execute(query)
        payment_types = [{
            "type": row[0],
            "transactions": row[1],
            "totalIncome": row[2]
        } for row in db[0].fetchall()]

        return payment_types
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db[0].close()

@ordersRouter.get("/orders/showDebt", response_model=list)
async def read_orders(db=Depends(get_db)):  
    query = "SELECT * FROM orders WHERE orderType = 'Tally'"
    db[0].execute(query)
    orders = [{
        "OrderID": order[0],
        "orderItem": order[1],
        "orderType": order[2],
        "orderDate": order[3],
        "orderTime": str(timedelta(seconds=order[4].seconds)),  # Convert time duration to string
        "orderTotal": order[5]
    } for order in db[0].fetchall()]
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

# -------------------CREATE----------------------------------
@ordersRouter.post("/orders/", response_model=dict)
async def create_order(
    order_items: str = Form(...),
    order_type: str = Form(...),
    order_total: int = Form(...),
    db=Depends(get_db)
):
    try:
        current_date = datetime.now().date()
        current_time = datetime.now().time()

        # Fetching the current maximum order ID
        db[0].execute("SELECT MAX(OrderID) FROM orders")
        max_order_id = db[0].fetchone()[0]
        if max_order_id is None:
            max_order_id = 0

        # Incrementing the order ID for the new order
        order_id = max_order_id + 1

        # Inserting the order into the database with the calculated order ID
        insert_query = "INSERT INTO orders (OrderID, OrderItems, OrderType, OrderDate, OrderTime, OrderTotal) VALUES (%s, %s, %s, %s, %s, %s)"
        db[0].execute(insert_query, (order_id, order_items, order_type, current_date, current_time, order_total))
        db[1].commit()

        return { 
            "orderID": order_id,
            "orderItems": order_items,
            "orderType": order_type,
            "orderDate": current_date,
            "orderTime": current_time,
            "orderTotal": order_total
        }
    except mysql.connector.Error as e:
        db[1].rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
    finally:
        db[0].close()
        
#--------------------UPDATE----------------------
@ordersRouter.put("/orders/{order_id}",response_model=dict)

async def update_order(
    OrderID: int,
    orderStatus: str, 
    orderDate: str, 
    orderTime: str, 
    orderTotal: int, 
    db= Depends(get_db)):
    try:
        # Update the order
        query = "UPDATE orders SET orderStatus = %s, orderDate = %s, orderTime = %s, orderTotal = %s WHERE OrderID = %s"
        db[0].execute(query, (OrderID,orderStatus,orderDate,orderTime,orderTotal))

    # Check if the update was successful
        if db[0].rowcount > 0:
         db[1].commit()
        
        return {"message": "Order updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db[0].close()




    # --------- DELETE---------------------------------

@ordersRouter.delete("/orders/{order_id}", response_model=dict)
async def delete_order(
    order_id: int,
    db=Depends(get_db)
):
    try:
        query_check_order = "SELECT OrderID FROM orders WHERE OrderID = %s"
        db[0].execute(query_check_order, (order_id,))
        existing_order = db[0].fetchone()

        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")

        query_delete_order = "DELETE FROM orders WHERE OrderID = %s"
        db[0].execute(query_delete_order, (order_id,))
        db[1].commit()
        return {"message": "Order deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
