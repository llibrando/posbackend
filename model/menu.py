# model/menu.py
from fastapi import Depends, HTTPException, APIRouter, UploadFile, File, Form, Header
from .db import get_db
from pydantic import BaseModel
import os


class MenuItem(BaseModel):
    menuItemCategory: str
    menuItemName: str
    menuItemPrice: int

menuRouter = APIRouter(tags=["Menu"])

# CRUD operations 

@menuRouter.get("/menu/", response_model=list)
async def read_menu(
    db=Depends(get_db)
):
    query = "SELECT ItemID,menuItemCategory, menuItemName, menuItemPrice, menuItemPic FROM menu"
    db[0].execute(query)
    menu = [{"ItemID": menu[0], "menuItemCategory":menu[1], "menuItemName": menu[2],"menuItemPrice": menu[3],"menuItemPic": menu[4]} for menu in db[0].fetchall()]
    return menu

@menuRouter.get("/menu/showsnacks", response_model=list)
async def read_showsnacks(
        db=Depends(get_db)
    ):
        query = "SELECT * FROM showsnacks"
        db[0].execute(query)
        showsnacks = [{"ItemID": showsnacks[0], "menuItemCategory":showsnacks[1], "menuItemName": showsnacks[2],"menuItemPrice": showsnacks[3]} for showsnacks in db[0].fetchall()]
        return showsnacks

@menuRouter.get("/menu/showdesserts", response_model=list)
async def read_showsdesserts(
        db=Depends(get_db)
    ):
        query = "SELECT * FROM showdesserts"
        db[0].execute(query)
        showdesserts = [{"ItemID": showdesserts[0], "menuItemCategory":showdesserts[1], "menuItemName": showdesserts[2],"menuItemPrice": showdesserts[3]} for showdesserts in db[0].fetchall()]
        return showdesserts

@menuRouter.get("/menu/showmeals", response_model=list)
async def read_showmeals(
        db=Depends(get_db)
    ):
        query = "SELECT * FROM showmeals"
        db[0].execute(query)
        showmeals = [{"ItemID": showmeals[0], "menuItemCategory":showmeals[1], "menuItemName": showmeals[2],"menuItemPrice": showmeals[3]} for showmeals in db[0].fetchall()]
        return showmeals

@menuRouter.get("/menu/showdrinks", response_model=list)
async def read_showdrinks(
        db=Depends(get_db)
    ):
        query = "SELECT * FROM showdrinks"
        db[0].execute(query)
        showdrinks = [{"ItemID": showdrinks[0], "menuItemCategory":showdrinks[1], "menuItemName": showdrinks[2],"menuItemPrice": showdrinks[3]} for showdrinks in db[0].fetchall()]
        return showdrinks

@menuRouter.get("/menu/{ItemID}", response_model=dict)
async def read_menu(ItemID: int, db=Depends(get_db)):
    try:
        query = "SELECT ItemID, menuItemCategory, menuItemName, menuItemPrice FROM menu WHERE ItemID = %s"
        db[0].execute(query, (ItemID,))
        menu = db[0].fetchone()
        if menu:
            return {
                "ItemID": menu[0],
                "menuItemCategory": menu[1],
                "menuItemName": menu[2],
                "menuItemPrice": menu[3]
            }
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        
# -----------------------------POST/CREATE----------------------------------
@menuRouter.post("/menu/", response_model=MenuItem)
async def create_menu_item(
    menuItemCategory: str = Form(...),
    menuItemName: str = Form(...),
    menuItemPrice: int = Form(...),
    menuItemPic: str = Form(...),
    db=Depends(get_db)
):
    try:
        # Insert the new item into the database without providing menuItemID
        query_insert_item = "INSERT INTO menu (menuItemCategory, menuItemName, menuItemPrice, menuItemPic) VALUES (%s, %s, %s, %s)"
        db[0].execute(query_insert_item, (menuItemCategory, menuItemName, menuItemPrice, menuItemPic))
        db[1].commit()



        return {"menuItemCategory": menuItemCategory, "menuItemName": menuItemName, "menuItemPrice": menuItemPrice, "menuItemPic": menuItemPic}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db[0].close()


# ----------------PUT/UPDATE------------------------------------------------
@menuRouter.put("/menu/{menuItemID}", response_model=dict)
async def update_order( 
    menuItemID: int,  
    menuItemCategory: str = Form(...),
    menuItemName: str = Form(...),
    menuItemPrice: int = Form(...),
    menuItemPic: str = Form(...),  # Keep it as a string
    db=Depends(get_db)
):
    print("Received item ID:", menuItemID)

    # Check if the item exists in the database before attempting to update
    query = "SELECT * FROM menu WHERE ItemID = %s"
    db[0].execute(query, (menuItemID,))
    existing_item = db[0].fetchone()

    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Debugging: Print existing item for verification
    print("Existing item:", existing_item)

    # Update menu information in the database 
    update_query = "UPDATE menu SET menuItemCategory = %s, menuItemName = %s, menuItemPrice = %s, menuItemPic = %s WHERE ItemID = %s"
    params = (menuItemCategory, menuItemName, menuItemPrice, menuItemPic, menuItemID)

    try:
        # Execute the update query
        db[0].execute(update_query, params)
        affected_rows = db[0].rowcount
        db[1].commit()
    except Exception as e:
        db[1].rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update item: {str(e)}")

    # Check if the update was successful
    if affected_rows > 0:
        return {"message": "Item updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Item update failed, no rows affected")



# --------------------DELETE--------------------------------
@menuRouter.delete("/menu/{menu_id}", response_model=dict)
async def delete_menu(
    menu_id: int,
    db=Depends(get_db)
):
    try:
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
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
