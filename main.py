# main.py
from fastapi import FastAPI
import mysql.connector
from model.cashier import cashierRouter
from model.menu import menuRouter
from model.payment import paymentRouter
from model.orders import ordersRouter
from model.transaction import transactionRouter


app = FastAPI()

# Include CRUD routes from modules
app.include_router(cashierRouter, prefix="/api")
app.include_router(menuRouter, prefix="/api")
app.include_router(ordersRouter, prefix="/api")
app.include_router(transactionRouter, prefix="/api")
app.include_router(paymentRouter, prefix="/api")


