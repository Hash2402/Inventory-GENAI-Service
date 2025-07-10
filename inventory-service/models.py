from pydantic import BaseModel
# Defines Pydantic models for validating inventory update requests.
class InventoryUpdate(BaseModel):
    item:str
    change:int