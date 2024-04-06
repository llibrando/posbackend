# model/transaction.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import bcrypt

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


# @transactionRouter.post("/transaction/", response_model=transactionCreate)
# async def create_transaction(transaction: transactionCreate, db=Depends(get_db)):
#     try:
#         # Construct the SQL query to insert a new transaction
#         query = "INSERT INTO transaction (username, password) VALUES (%s, %s)"
#         # Execute the query with the provided data
#         db[0].execute(query, (transaction.username, transaction.password))
#         # Commit the transaction
#         db[1].commit()
#         # Return the created transaction
#         return transaction
#     except Exception as e:
#         # If an error occurs, raise an HTTPException with a 500 status code
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
#     finally:
#         # Close the cursor and database connection
#         db[0].close()



# ----------------PUT/UPDATE------------------------------------------------
@transactionRouter.put("/transaction/{trans_id}", response_model=dict)
async def update_transaction(
    trans_id: int,
    ItemID: int,
    OrderID: int,
    SubTotal: float,
    db=Depends(get_db)
):

    # Update transaction information in the database 
    query = "UPDATE transaction SET ItemID = %s, OrderID = %s, SubTotal =%s  WHERE TransactionID = %s"
    db[0].execute(query, (ItemID, OrderID, SubTotal, trans_id))

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
