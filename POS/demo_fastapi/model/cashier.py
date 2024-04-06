from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from .db import get_db 
import bcrypt
import mysql.connector

class CashierUpdate(BaseModel):
    username: str
    password: str
class CashierCreate(BaseModel):
    username: str
    password: str

CashierRouter = APIRouter()
CashierRouter = APIRouter(tags=["cashier"])

#GET
@CashierRouter.get("/cashier", response_model=list)
async def get_cashiers(db=Depends(get_db)):
    try:
        # Modify the query to select only the username and cashierID fields
        query = "SELECT cashierID, username FROM cashier"
        db[0].execute(query)
        cashiers = db[0].fetchall()
        return cashiers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db[0].close()
#GET CASHIERID
@CashierRouter.get("/cashier/{cashier_id}", response_model=dict) 
async def get_cashierid(cashierid: int, db=Depends(get_db)):
    try:
        query = "SELECT `cashierID`, `username` FROM `cashier` WHERE `cashierID` = %s"
        db[0].execute(query, (cashierid,))
        cashier = db[0].fetchone()

        if not cashier:
            raise HTTPException(status_code=404, detail="Cashier not found")

        return {
            "cashierID": cashier[0],
            "username": cashier[1],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db[0].close()

#CREATE
@CashierRouter.post("/cashier/", response_model=CashierCreate)
async def create_cashier(cashier: CashierCreate, db=Depends(get_db)):
    try:
        # Construct the SQL query to insert a new cashier
        query = "INSERT INTO cashier (username, password) VALUES (%s, %s)"
        # Execute the query with the provided data
        db[0].execute(query, (cashier.username, cashier.password))
        # Commit the transaction
        db[1].commit()
        # Return the created cashier
        return cashier
    except Exception as e:
        # If an error occurs, raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the cursor and database connection
        db[0].close()

#UPDATE
@CashierRouter.put("/cashier/{cashier_id}", response_model=dict)
async def update_cashier(cashier_id: int, cashier_update: CashierUpdate, db=Depends(get_db)):
    try:
        query_check_user = "SELECT `cashierID` FROM `cashier` WHERE `cashierID` = %s"
        db[0].execute(query_check_user, (cashier_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="Cashier not found")

        query_update_user = "UPDATE `cashier` SET `username` = %s, `password` = %s WHERE `cashierID` = %s"
        db[0].execute(query_update_user, (cashier_update.username, cashier_update.password, cashier_id))
        db[1].commit()

        return {"message": "Cashier updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db[0].close()

#DELETE
@CashierRouter.delete("/cashier/{cashier_id}")
async def delete_cashier(cashier_id: int, db=Depends(get_db)):
    try:
        # Check if the cashier exists
        query_check_cashier = "SELECT cashierID FROM cashier WHERE cashierID = %s"
        db[0].execute(query_check_cashier, (cashier_id,))
        existing_cashier = db[0].fetchone()

        # If the cashier does not exist, raise HTTPException with 404 status code
        if not existing_cashier:
            raise HTTPException(status_code=404, detail="Cashier not found")

        # Delete the cashier from the database
        query_delete_cashier = "DELETE FROM cashier WHERE cashierID = %s"
        db[0].execute(query_delete_cashier, (cashier_id,))
        db[1].commit()

        # Return success message
        return {"message": "Cashier deleted successfully"}
    except Exception as e:
        # If an error occurs, raise HTTPException with 500 status code
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the cursor and database connection
        db[0].close()

def hash_password(password: str):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Decode bytes to string for storage