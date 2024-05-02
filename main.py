# main.py
from fastapi import FastAPI
import mysql.connector
from model.cashier import cashierRouter
from model.menu import menuRouter
from model.payment import paymentRouter
from model.orders import ordersRouter
from model.transaction import transactionRouter
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

# Include CRUD routes from modules
app.include_router(cashierRouter, prefix="/api")
app.include_router(menuRouter, prefix="/api")
app.include_router(ordersRouter, prefix="/api")
app.include_router(transactionRouter, prefix="/api")
app.include_router(paymentRouter, prefix="/api")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)