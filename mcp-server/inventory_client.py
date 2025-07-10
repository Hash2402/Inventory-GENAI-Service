import httpx
from fastapi import HTTPException
INVENTORY_API_URL="http://localhost:8000/inventory"

async def get_inventory():
    async with httpx.AsyncClient() as client:
        response = await client.get(INVENTORY_API_URL)
        response.raise_for_status()
        return response.json()
    
async def post_inventory(item: str, change: int):
    try:
        response = httpx.post("http://localhost:8000/inventory", json={
            "item": item,
            "change": change
        })
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        # Relay error message from inventory-service
        error_detail = e.response.json().get("detail", "Unknown error")
        raise HTTPException(status_code=400, detail=f"Inventory update failed: {error_detail}")
    