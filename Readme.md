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
## System Design

![Screenshot 2025-07-09 232747](https://github.com/user-attachments/assets/44428229-bd9a-4397-b520-b6f92165348f)

### Component Responsibilities
| Component             | Description                                                                                                     |
| --------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Inventory Service** | Manages inventory state, exposes `/inventory` GET/POST APIs. Persists data to `inventory.json`.                 |
| **MCP Server**        | Receives user messages, uses OpenRouter LLM to convert input into structured actions, then calls Inventory API. |
| **MCP Client (CLI)**  | Optional. A simple terminal-based interface to talk to MCP Server.                                              |

### Interaction Flow
#### Example:
1. User says: “I sold 2 pants”  

2. MCP Client sends this message to MCP Server.  

3. MCP Server uses LLM (via OpenRouter) to convert it to:  
   
```
{ 
"action": "POST",
 "request":
  {
    "item": "pants",
    "change": -2
  }
}
```  

4. MCP Server sends this to Inventory Service's /inventory endpoint.  

5. Inventory Service checks if the transaction is possible and updates the inventory

6. Inventory Service responds with the new state.  

7. MCP returns this state to user.  

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

![Screenshot 2025-07-09 224123](https://github.com/user-attachments/assets/f6547e53-dec1-4256-98b7-380e58d32d72)

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

![Screenshot 2025-07-09 225403](https://github.com/user-attachments/assets/39eb83cd-5464-4d1e-bb35-19ea52df30c4)


#### ➤ MCP API Endpoint:
```
POST http://localhost:8001/mcp
Content-Type: application/json
Body: { "message": "I sold 3 pants" }
````
---
##  Example Natural Language Inputs

| Input Message                          | Action Taken                        |
| -------------------------------------- | ----------------------------------- |
| `I sold 3 tshirts`                     | POST `/inventory` with `change: -3` |
| `Add 5 pants`                          | POST `/inventory` with `change: +5` |
| `How many pants and shirts do I have?` | GET `/inventory`                    |

---
## Testing Using Postman
#### You can easily test the Inventory Service and MCP Server APIs using Postman by following these steps:

#### 1. Testing Inventory Service
#### Get current inventory
```
Method: GET
```
```
URL: http://localhost:8000/inventory
```

   * Click Send

   * You should see JSON response with current counts, e.g.:
```
{
  "tshirts": 20,
  "pants": 19
}
```
![Screenshot 2025-07-09 224220](https://github.com/user-attachments/assets/963f6d2b-0673-482f-b5bc-5710424428a8)

####  Modify inventory
```
Method: POST
```
```
URL: http://localhost:8000/inventory
```
```
Body (raw, JSON):
{
  "item": "tshirts",
  "change": -5
}
```
* Click Send

* The response shows updated inventory counts.
  
  ![Screenshot 2025-07-09 224341](https://github.com/user-attachments/assets/022b4269-8e4f-46a9-a46a-d70193f2602e)

## 2. Testing MCP Server
#### Send a natural language query
```
Method: POST
```
```
URL: http://localhost:8001/mcp
```
```
Body (raw, JSON):
{
  "message": "How many pants and shirts do I have?"

}
```
* Click Send

* The response will show interpreted action and updated inventory, for example:
```
{
  "action": "GET",
  "response": {
    "tshirts": 15,
    "pants": 19
  }
}
```
![Screenshot 2025-07-09 224607](https://github.com/user-attachments/assets/5e0a679c-9559-47a7-bc7e-9de80141cc1d)

#### Try other natural language commands, such as:
```
"Add 5 tshirts"
```

![Screenshot 2025-07-09 224646](https://github.com/user-attachments/assets/8645218e-296c-412a-be9a-32fec00dac93)
---
## Bonus: CLI Client + Batch Script
### mcp-client/cli.py

This is a small interactive command-line client to test MCP natural language queries from terminal.

```
cd mcp-client
python cli.py
```
---

![Screenshot 2025-07-09 230310](https://github.com/user-attachments/assets/c2a9d2b2-2fd0-4602-8649-0b376d0339fa)

### start_all.bat
Run all services in one go by clicking on start_all.bat (WINDOWS OS)

#### It launches:
+ Inventory service (port 8000)

+ MCP service (port 8001)

+ MCP CLI in third window

  ![Screenshot 2025-07-09 224850](https://github.com/user-attachments/assets/c45f52d8-2a65-4bff-818c-585c5184da49)

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
* Develop a clean and User Freindly dashborad for ease of access

* Migrate to SQLite/PostgreSQL for persistence

* Add authentication and role-based access

* Expand GenAI prompt logic using LangChain or structured output parsers
---
## Conclusion
This project combines REST APIs, file-based persistence, and GenAI-powered logic control through a clean and modular design. It showcases backend fundamentals and AI integration through OpenRouter and OpenAPI prompting.
