# model/cashier.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from .db import get_db 
from typing import Optional
from pydantic import BaseModel
import mysql.connector
import bcrypt
cashierRouter = APIRouter(tags=["cashier"]) 

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
@cashierRouter.post("/cashier/",  response_model=dict)
async def create_cashier(
     cashierID: int= Form(...), 
     username: str= Form(...), 
      password: str= Form(...), 
      db=Depends(get_db)):
    try:
        
        query = "INSERT INTO cashier (cashierID, username, password) VALUES (%s, %s,%s)"
        # Execute the query with the provided data
        db[0].execute(query,(cashierID, username,password))
        db[1].commit()
        cashierID = db[0].lastrowid
        return {
            "CashierID": cashierID, 
            "Username": username,
            "Password": password,    
            }
    except Exception as e:
        # If an error occurs, raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the cursor and database connection
        db[0].close()


# -------------------------------PUT/UPDATE---------------------------------------------
@cashierRouter.put("/cashier/{cashier_id}", response_model=dict)
async def update_cashier(cashierID:int= Form(...), 
    username: str= Form(...), 
    password: str= Form(...),  db=Depends(get_db)):
    try:
        query_update_user = "UPDATE cashier SET username = %s, password = %s WHERE cashierID = %s"
        db[0].execute(query_update_user, (cashierID,username,password))
        db[1].commit()
        return {
            "CashierID": cashierID, 
            "Username": username,
            "Password": password,    
            }
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


