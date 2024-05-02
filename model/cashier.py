# model/cashier.py
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
from .db import get_db 
from typing import Optional
from pydantic import BaseModel, validator
import mysql.connector
from cryptography.fernet import Fernet
import bcrypt
import os

key = b'YrAv2bNkJ1gkE5F15tclnM_1toW_5-FK0LjSafE2xhE='

# Initialize the Fernet cipher suite after ensuring the secret key is set
cipher_suite = Fernet(key)

class CashierUpdate(BaseModel):
    cashierID: int
    username: str
    password: str

class CashierCreate(BaseModel):
    cashierID: int
    username: str
    password: str

    @validator('password')
    def hash_password(cls, password):
        # Encrypt the password using Fernet
        encrypted_password = cipher_suite.encrypt(password.encode('utf-8'))
        return encrypted_password.decode('utf-8')

class User(BaseModel):
    username: str
    password: str

cashierRouter = APIRouter(tags=["Cashier"]) 

# CRUD operation

@cashierRouter.get("/cashier/", response_model=list)
async def read_cashier(
    db=Depends(get_db)
):
    query = "SELECT cashierID, username, password FROM cashier"
    db[0].execute(query)
    cashier = [{"cashierID": cashier[0], "username": cashier[1], "password": cashier[2]} for cashier in db[0].fetchall()]
    return cashier


@cashierRouter.get("/cashier/{CashierID}", response_model=dict)
async def read_cashier(
    CashierID: int, 
    db=Depends(get_db)
):
    query = "SELECT cashierID, username FROM cashier WHERE cashierID = %s"
    db[0].execute(query, (CashierID,))
    cashier = db[0].fetchone()
    if cashier:                             
        return {
            "cashierID": cashier[0],
            "username": cashier[1],
        }
    raise HTTPException(status_code=404, detail="Cashier not found")




# --------------------POST---------------------------------------------------------------
@cashierRouter.post("/cashier/", response_model=CashierCreate)
async def create_cashier(cashier: CashierCreate, db=Depends(get_db)):
    try:
        # Encrypt the password using Fernet
        encrypted_password = cipher_suite.encrypt(cashier.password.encode())

        # Construct the SQL query to insert a new cashier
        query = "INSERT INTO cashier (cashierID, username, password) VALUES (%s, %s,%s)"

        # Execute the query with the provided data
        db[0].execute(query, (cashier.cashierID, cashier.username, encrypted_password.decode()))

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

# -------------------------------PUT/UPDATE---------------------------------------------
@cashierRouter.put("/cashier/{cashier_id}", response_model=dict)
async def update_cashier(cashier_id: int, cashier_update: CashierUpdate, db=Depends(get_db)):
    try:
        query_check_user = "SELECT cashierID, username, password FROM cashier WHERE cashierID = %s"
        db[0].execute(query_check_user, (cashier_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="Cashier not found")

        query_update_user = "UPDATE cashier SET username = %s, password = %s WHERE cashierID = %s"
        db[0].execute(query_update_user, (cashier_update.username, cashier_update.password, cashier_id))
        db[1].commit()

        return {"message": "Cashier updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db[0].close()




# -------------------DELETE------------------------------------------------------
@cashierRouter.delete("/cashier/{cashier_id}")
async def delete_cashier(cashier_id: int, 
                        db=Depends(get_db)):
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

# -------------------LOGIN------------------------------------------------------
@cashierRouter.post("/login")
async def login(user: User, db=Depends(get_db)):
    try:
        query = "SELECT username, password FROM cashier WHERE username = %s"
        db[0].execute(query, (user.username,))
        result = db[0].fetchone()

        if result:
            stored_username = result[0]  # Extract username from tuple
            stored_password = result[1]  # Extract encrypted password from tuple

            # Log stored password hash and input password for debugging
            print(f"Stored encrypted password: {stored_password}")
            print(f"Input password: {user.password}")

            # Try to decrypt the stored password if it's not empty
            if stored_password:
                print("Decrypting password...")
                try:
                    print("Decryption Trying.")
                    decrypted_password = cipher_suite.decrypt(stored_password)
                    decrypted_password = decrypted_password.decode()
                    print("Decryption successful.")
                except Exception as decrypt_error:
                    print(f"Decryption failed: {str(decrypt_error)}")
                    raise HTTPException(status_code=500, detail="Internal Server Error: Decryption failed")

                # Compare the stored decrypted password with the input password
                if decrypted_password == user.password:
                    return {"message": "Login successful"}
                else:
                    raise HTTPException(status_code=401, detail="Invalid username or password")
            else:
                raise HTTPException(status_code=401, detail="Invalid username or password")
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception as e:
        print(f"Exception: {str(e)}")  # Print the exception for debugging
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db[0].close()