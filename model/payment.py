# model/payment.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import bcrypt
from pydantic import BaseModel

paymentRouter = APIRouter(tags=["Payment"])
# CRUD operation

@paymentRouter.get("/payment/", response_model=list)
async def read_payment(
    db=Depends(get_db)
):
    query = "SELECT PaymentID, PaymentType FROM payment"
    db[0].execute(query)
    payment = [{"paymentID": payment[0], "paymentType": payment[1]} for payment in db[0].fetchall()]
    return payment


@paymentRouter.get("/payment/{PaymentID}", response_model=dict)
async def read_payment(
    PaymentID: int, 
    db=Depends(get_db)
):
    query = "SELECT PaymentID, PaymentType FROM payment WHERE PaymentID = %s"
    db[0].execute(query, (PaymentID,))
    payment = db[0].fetchone()
    if payment:                             
        return {"PaymentID": payment[0],
                "PaymentType": payment[1]}
    raise HTTPException(status_code=404, detail="Payment not found")




# -----------------------------POST/CREATE----------------------------------

@paymentRouter.post("/payment/", response_model=dict)
async def create_payment(
    payment_id: int ,  
    PaymentType: str ,
    db=Depends(get_db)
):
 try:
    query = "INSERT INTO payment (PaymentID, PaymentType) VALUES (%s, %s)"
    db[0].execute(query, (payment_id,PaymentType))
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"PaymentID": payment_id, 
            "PaymentType": PaymentType,  
             }
 except Exception as e:
        # If an error occurs, raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
 finally:
        # Close the cursor and database connection
        db[0].close()





# -------------------------------PUT/UPDATE------------------------
@paymentRouter.put("/payment/{payment_id}", response_model=dict)
async def update_payment(
    PaymentID: int,
    PaymentType: str,
    db=Depends(get_db)
):
 try:
    # Update payment information in the database 
    query = "UPDATE payment SET PaymentType = %s  WHERE PaymentID = %s"
    db[0].execute(query, ( PaymentType, PaymentID))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Payment updated successfully"}
    
    # If no rows were affected, cashier not found
    raise HTTPException(status_code=404, detail="Payment not found")
 except Exception as e:
        # If an error occurs, raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
 finally:
        # Close the cursor and database connection
        db[0].close()





# ---------------------------DELETE-------------------------check
@paymentRouter.delete("/payment/{payment_id}", response_model=dict)
async def delete_payment(
    payment_id: int,
    db=Depends(get_db)
):
 try:
        # Check if the cashier exists
        query_check_payment = "SELECT PaymentID FROM payment WHERE PaymentID = %s"
        db[0].execute(query_check_payment, (payment_id,))
        existing_payment = db[0].fetchone()

        if not existing_payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        # Delete the cashier
        query_delete_payment = "DELETE FROM payment WHERE PaymentID = %s"
        db[0].execute(query_delete_payment, (payment_id,))
        db[1].commit()

        return {"message": "Payment deleted successfully"}
 except Exception as e:
        # If an error occurs, raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
 finally:
        # Close the cursor and database connection
        db[0].close()
