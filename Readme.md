# Inventory Management + GenAI Interface

## Overview

This project implements an Inventory Management system with two components:

1. **Inventory Service**: A REST API managing inventory counts of `tshirts` and `pants`.
2. **MCP Server (Model Control Plane)**: A GenAI-powered interface that interprets natural language commands to interact with the Inventory Service.

---

## Project Structure
```
root/
├── inventory-service/                  # Inventory backend service
│   ├── main.py                         # FastAPI app for inventory management
│   ├── inventory.py                    # Business logic and JSON persistence
│   ├── models.py                       # Pydantic model for request validation
│   ├── inventory.json                  # Persistent data file
│   └── requirements.txt                # Dependencies
│
├── mcp-server/                         # GenAI-powered MCP service
│   ├── main.py                         # FastAPI server using LLM to interpret natural language
│   ├── utils.py                        # OpenRouter API call logic
│   ├── inventory_client.py             # Handles calling inventory service
│   ├── prompts.py                      # System prompts/instructions for LLM
│   ├── .env                            # Stores OpenRouter API key and model name
│   └── requirements.txt                # Dependencies
│
├── mcp-client/                         #  Bonus: CLI Client
│   └── cli.py                          # Command-line interface to interact with MCP
│
├── openapi.yaml                        # OpenAPI schema (used to help LLM format responses)
├── start_all.bat                       # Bonus: Script to run all components in new terminal tabs
└── README.md                           # Documentation and setup instructions
```
---

##  Setup Instructions

###  Prerequisites

- Python 3.9+
- Recommended: create a virtual environment

---

###  1. Inventory Service

#### ➤ Navigate to folder:

```cd inventory-service```

#### ➤ Install dependencies:

```pip install -r requirements.txt```

#### ➤ Run the service:
```uvicorn main:app --reload --port 8000```

+ Data is auto-loaded from inventory.json if it exists.

+ After every change, the updated inventory is saved.

+ Swagger/OpenAPI docs: http://localhost:8000/docs

### 2. MCP Server (Model Control Plane)
#### ➤ Navigate to folder:
```cd mcp-server```

#### ➤ Add .env file:
```
OPENROUTER_API_KEY="YOUR-OPENROUTER-KEY"  
MODEL=mistralai/mistral-small-3.2-24b-instruct:free
```
#### ➤ Install dependencies:
```pip install -r requirements.txt```

#### ➤ Run the server:
```uvicorn main:app --reload --port 8001```

#### ➤ MCP API Endpoint:
```
POST http://localhost:8001/mcp
Content-Type: application/json
Body: { "message": "I sold 3 pants" }
````

##  Example Natural Language Inputs

| Input Message                          | Action Taken                        |
| -------------------------------------- | ----------------------------------- |
| `I sold 3 tshirts`                     | POST `/inventory` with `change: -3` |
| `Add 5 pants`                          | POST `/inventory` with `change: +5` |
| `How many pants and shirts do I have?` | GET `/inventory`                    |




## Bonus: CLI Client + Batch Script
### mcp-client/cli.py

This is a small interactive command-line client to test MCP natural language queries from terminal.

```
cd mcp-client
python cli.py
```
---

### start_all.bat
Run all services in one go by clicking on start_all.bat (WINDOWS OS)

#### It launches:
+ Inventory service (port 8000)

+ MCP service (port 8001)

+ MCP CLI in third window
---

##  OpenAPI Integration
* openapi.yaml describes the REST interface of the inventory service

* The prompts.py in MCP uses this schema to instruct the LLM how to call the backend correctly

* Helps convert vague user queries into structured JSON actions
---
##  Tech Stack
* Python 3.10

* FastAPI – REST API framework

* httpx – Async HTTP calls

* OpenRouter – LLM-based natural language interpretation

* Pydantic – Data validation

* dotenv – Secure API key management

* Uvicorn – ASGI server
---
##  Limitations
* Inventory is saved in a JSON file, not a database

* Only supports tshirts and pants

* No authentication implemented

* GenAI responses depend on LLM prompt tuning and API model availability
---
##  Future Improvements
* Add SKU-based inventory with item metadata

* Migrate to SQLite/PostgreSQL for persistence

* Add authentication and role-based access

* Expand GenAI prompt logic using LangChain or structured output parsers
---
## Conclusion
This project combines REST APIs, file-based persistence, and GenAI-powered logic control through a clean and modular design. It showcases backend fundamentals and AI integration through OpenRouter and OpenAPI prompting.
