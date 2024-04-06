# model/transaction.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import bcrypt
from fastapi import FastAPI

transactionRouter = APIRouter(tags=["Transaction"])


# CRUD operations

@transactionRouter.get("/transaction/", response_model=list)
async def read_transaction(
    db=Depends(get_db)
):
    query = "SELECT transactionID, Subtotal FROM transaction"
    db[0].execute(query)
    transaction = [{"transactionID": transaction[0], "Subtotal": transaction[1]} for transaction in db[0].fetchall()]
    return transaction


@transactionRouter.get("/transaction/{transactionID}", response_model=dict)
async def read_transaction_by_id(
    ItemID: int, 
    db=Depends(get_db)
):
    query = "SELECT transactionID, Subtotal FROM transaction WHERE transactionID = %s"
    db[0].execute(query, (ItemID,))
    transaction = db[0].fetchone()
    if transaction:                             
        return {
            "transactionID": transaction[0],
            "Subtotal": transaction[1],
        }
    raise HTTPException(status_code=404, detail="Transaction not found")



# -----------------------------POST/CREATE----------------------------------

@transactionRouter.post("/transaction/", response_model=dict)
async def create_transaction(
    transaction_id: int, 
    item_id: int, 
    sub_total: float,  
    db=Depends(get_db)
):

    query = "INSERT INTO transaction (TransactionID, ItemID, SubTotal) VALUES ( %s, %s, %s)"
    db[0].execute(query, (transaction_id, item_id, sub_total))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {
        "TransactionID": transaction_id, 
        "ItemID": item_id,
        "SubTotal": sub_total,     
    }


# ----------------PUT/UPDATE------------------------------------------------


@transactionRouter.put("/transaction/{transactionid}", response_model=dict)
async def update_transaction(
    transactionid: int,
    item_id: int,
    order_id: int,
    SubTotal: float,
    db=Depends(get_db)
):

    # Update cashier information in the database 
    query = "UPDATE transaction SET ItemID = %s, OrderID = %s, SubTotal = %s  WHERE TransactionID = %s"
    db[0].execute(query, (item_id, order_id, SubTotal, transactionid))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "transaction updated successfully"}
    
    # If no rows were affected, cashier not found
    raise HTTPException(status_code=404, detail="transaction not found")


# -----------------DELETE-------------------------------------
@transactionRouter.delete("/transaction/{transaction_id}", response_model=dict)
async def delete_transaction(
    transaction_id: int,
    db=Depends(get_db)
):
    # try:
        # Check if the item  exists
        query_check_transaction = "SELECT TransactionID FROM transaction WHERE TransactionID = %s"
        db[0].execute(query_check_transaction, (transaction_id,))
        existing_transaction = db[0].fetchone()

        if not existing_transaction:
            raise HTTPException(status_code=404, detail="transaction not found")

        # Delete the item
        query_delete_transaction = "DELETE FROM transaction WHERE TransactionID = %s"
        db[0].execute(query_delete_transaction, (transaction_id,))
        db[1].commit()

        return {"message": "transaction deleted successfully"}
