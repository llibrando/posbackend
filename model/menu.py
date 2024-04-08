# model/menu.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import bcrypt

menuRouter = APIRouter(tags=["Menu"])

# CRUD operations

@menuRouter.get("/menu/", response_model=list)
async def read_menu(
    db=Depends(get_db)
):
    query = "SELECT ItemID, menuItemName FROM menu"
    db[0].execute(query)
    menu = [{"ItemID": menu[0], "menuItemName": menu[1]} for menu in db[0].fetchall()]
    return menu


@menuRouter.get("/menu/{ItemID}", response_model=dict)
async def read_menu(
    ItemID: int, 
    db=Depends(get_db)
):
    query = "SELECT ItemID, menuItemName FROM menu WHERE ItemID = %s"
    db[0].execute(query, (ItemID,))
    menu = db[0].fetchone()
    if menu:                             
        return {
            "ItemID": menu[0],
            "menuItemName": menu[1],
        }
    raise HTTPException(status_code=404, detail="Item not found")


# -----------------------------POST/CREATE----------------------------------

@menuRouter.post("/menu/", response_model=dict)
async def create_item(
    item_id: int = Form(...), 
    menuItemCategory: str = Form(...), 
    menuItemName: str = Form(...),
    menuItemPrice: int = Form(...),  
    db=Depends(get_db)
):

    query = "INSERT INTO menu (ItemID, menuItemCategory, menuItemName, menuItemPrice) VALUES (%s, %s, %s, %s)"
    db[0].execute(query, (item_id, menuItemCategory, menuItemName, menuItemPrice))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"item_id": new_user_id, 
            "menuItemCategory": menuItemCategory,
            "menuItemName": menuItemName,
            "menuItemPrice": menuItemPrice,     
            }




# ----------------PUT/UPDATE------------------------------------------------
@menuRouter.put("/menu/{menu_id}", response_model=dict)
async def update_order(
    menu_id: int,
    menuItemCategory: str,
    menuItemName: str,
    menuItemPrice: int,
    db=Depends(get_db)
):

    # Update menu information in the database 
    query = "UPDATE menu SET menuItemCategory = %s, menuItemName = %s, menuItemPrice =%s  WHERE ItemID = %s"
    db[0].execute(query, (menuItemCategory, menuItemName, menuItemPrice, menu_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Item updated successfully"}
    
    # If no rows were affected, cashier not found
    raise HTTPException(status_code=404, detail="Item not found")





# --------------------DELETE--------------------------------
@menuRouter.delete("/menu/{menu_id}", response_model=dict)
async def delete_menu(
    menu_id: int,
    db=Depends(get_db)
):
    # try:
        # Check if the item exists
        query_check_menu = "SELECT ItemID FROM menu WHERE ItemID = %s"
        db[0].execute(query_check_menu, (menu_id,))
        existing_item = db[0].fetchone()

        if not existing_item:
            raise HTTPException(status_code=404, detail="Item not found")

        # Delete the item
        query_delete_item = "DELETE FROM menu WHERE ItemID = %s"
        db[0].execute(query_delete_item, (menu_id,))
        db[1].commit()

        return {"message": "Item deleted successfully"}
