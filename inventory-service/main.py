from fastapi import FastAPI,HTTPException
from models import InventoryUpdate

from inventory import (
    get_inventory,
    update_inventory,
    load_inventory
)

#load Inventory on startup
load_inventory()

app=FastAPI(title="Inventory Service",version="1.0.0")

@app.get("/inventory")
def read_inventory():
    """
    Uses the get_inventory funciton from inventory.py to return the current inventory.
    """
    return get_inventory()

@app.post("/inventory")
def modify_inventory(update:InventoryUpdate):
    """
    Uses updater_inventory function to make changes to the inventory data
    """
    try:
        return update_inventory(update.item.lower(),update.change)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))