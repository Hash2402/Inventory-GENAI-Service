""" import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

from utils import interpret_query
from inventory_client import get_inventory, post_inventory

app = FastAPI(title="MCP Server", version="1.0.0")

# Load OpenAPI spec once when app starts
with open("openapi.yaml", "r") as f:
    openapi_spec = yaml.safe_load(f)

print("Loaded OpenAPI paths:", list(openapi_spec["paths"].keys()))

class MCPRequest(BaseModel):
    message: str

@app.post("/mcp")
async def process_message(req: MCPRequest):
    user_msg = req.message
    try:
        llm_response = await interpret_query(user_msg)  
        llm_response = llm_response.strip()
        if llm_response.startswith("```json"):
            llm_response = llm_response.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(llm_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM processing failed: {str(e)}")

    action = parsed.get("action")
    request_body = parsed.get("request")

    if action == "GET":
        inventory = await get_inventory()
        return {"action": "GET", "response": inventory}

    elif action == "POST":
        if not isinstance(request_body, dict):
            raise HTTPException(status_code=400, detail="Invalid request body from LLM")
        item = request_body.get("item")
        change = request_body.get("change")
        if not item or not isinstance(change, int):
            raise HTTPException(status_code=400, detail="Missing or invalid fields in request")
        # You can here use `openapi_spec` to validate or dynamically build calls
        inventory = await post_inventory(item.lower(), change)
        return {"action": "POST", "request": request_body, "response": inventory}

    else:
        raise HTTPException(status_code=400, detail="Unsupported action from LLM")
 """
import yaml
import json
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from utils import interpret_query  # your LLM wrapper

app = FastAPI(title="MCP Server", version="1.0.0")

# Load OpenAPI spec once at startup
with open("../openapi.yaml", "r") as f:
    openapi_spec = yaml.safe_load(f)

INVENTORY_BASE_URL = "http://localhost:8000"  # adjust if needed

class MCPRequest(BaseModel):
    message: str

async def dynamic_get_inventory():
    path = "/inventory"
    method = "get"
    if path not in openapi_spec["paths"] or method not in openapi_spec["paths"][path]:
        raise Exception(f"API spec missing {method.upper()} {path}")

    url = INVENTORY_BASE_URL + path
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()

async def dynamic_post_inventory(item: str, change: int):
    path = "/inventory"
    method = "post"
    if path not in openapi_spec["paths"] or method not in openapi_spec["paths"][path]:
        raise Exception(f"API spec missing {method.upper()} {path}")

    url = INVENTORY_BASE_URL + path
    payload = {"item": item, "change": change}
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

@app.post("/mcp")
async def process_message(req: MCPRequest):
    user_msg = req.message
    try:
        llm_response = await interpret_query(user_msg)
        llm_response = llm_response.strip()
        if llm_response.startswith("```json"):
            llm_response = llm_response.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(llm_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM processing failed: {str(e)}")

    action = parsed.get("action")
    request_body = parsed.get("request")

    if action == "GET":
        inventory = await dynamic_get_inventory()
        return {"action": "GET", "response": inventory}

    elif action == "POST":
        if not isinstance(request_body, dict):
            raise HTTPException(status_code=400, detail="Invalid request body from LLM")
        item = request_body.get("item")
        change = request_body.get("change")
        if not item or not isinstance(change, int):
            raise HTTPException(status_code=400, detail="Missing or invalid fields in request")
        inventory = await dynamic_post_inventory(item.lower(), change)
        return {"action": "POST", "request": request_body, "response": inventory}

    else:
        raise HTTPException(status_code=400, detail="Unsupported action from LLM")
