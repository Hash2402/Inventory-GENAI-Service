from pydantic import BaseModel

class InventoryUpdate(BaseModel):
    item:str
    change:int