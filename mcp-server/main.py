import yaml
import json
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from utils import interpret_query  # your LLM wrapper

app = FastAPI(title="MCP Server", version="1.0.0")

# Load OpenAPI spec once at startup for dynamic API validation
with open("../openapi.yaml", "r") as f:
    openapi_spec = yaml.safe_load(f)

INVENTORY_BASE_URL = "http://localhost:8000"  # base URL for inventory service

class MCPRequest(BaseModel):
    message: str  # User's natural language input

async def dynamic_get_inventory():
    path = "/inventory"
    method = "get"
    # Validate that API spec has this GET path defined
    if path not in openapi_spec["paths"] or method not in openapi_spec["paths"][path]:
        raise Exception(f"API spec missing {method.upper()} {path}")

    url = INVENTORY_BASE_URL + path
    # Async GET request to inventory service
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()

async def dynamic_post_inventory(item: str, change: int):
    path = "/inventory"
    method = "post"
    # Validate that API spec has this POST path defined
    if path not in openapi_spec["paths"] or method not in openapi_spec["paths"][path]:
        raise Exception(f"API spec missing {method.upper()} {path}")

    url = INVENTORY_BASE_URL + path
    payload = {"item": item, "change": change}
    # Async POST request to update inventory
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

@app.post("/mcp")
async def process_message(req: MCPRequest):
    user_msg = req.message
    try:
        # Call LLM to interpret user natural language message
        llm_response = await interpret_query(user_msg)
        llm_response = llm_response.strip()
        # Remove markdown formatting if present
        if llm_response.startswith("```json"):
            llm_response = llm_response.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(llm_response)  # Parse LLM JSON response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM processing failed: {str(e)}")

    action = parsed.get("action")
    request_body = parsed.get("request")

    if action == "GET":
        inventory = await dynamic_get_inventory()
        return {"action": "GET", "response": inventory}

    elif action == "POST":
        # Validate parsed LLM request body fields
        if not isinstance(request_body, dict):
            raise HTTPException(status_code=400, detail="Invalid request body from LLM")
        item = request_body.get("item")
        change = request_body.get("change")
        if not item or not isinstance(change, int):
            raise HTTPException(status_code=400, detail="Missing or invalid fields in request")
        # Call inventory service to update inventory
        inventory = await dynamic_post_inventory(item.lower(), change)
        return {"action": "POST", "request": request_body, "response": inventory}

    else:
        raise HTTPException(status_code=400, detail="Unsupported action from LLM")
