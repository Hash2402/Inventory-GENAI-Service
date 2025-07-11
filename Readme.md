# Inventory Management + GenAI Interface
----

##  Table of Contents

+ [Overview](#overview)
+ [Project Structure](#project-structure)
+ [inventory-service/](#inventory-service)
+ [mcp-server/](#mcp-server)
+ [mcp-client/ (Optional CLI)](#mcp-client-optional-cli)
+ [openapi.yaml](#openapiyaml)
+ [start_all.bat (Bonus)](#start_allbat-bonus)
+ [System Design](#system-design)
+ [Setup Instructions](#setup-instructions)
+ [Example Natural Language Inputs](#example-natural-language-inputs)
+ [Testing Using Postman](#testing-using-postman)
+ [Bonus: CLI Client + Batch Script](#bonus-cli-client--batch-script)
+ [OpenAPI Integration](#openapi-integration)
+ [Tech Stack](#tech-stack)
+ [Limitations](#limitations)
+ [Future Improvements](#future-improvements)
+ [Experimentation & Design Decisions](#experimentation--design-decisions)
+ [Key Learnings](#key-learnings)
+ [Conclusion](#conclusion)
  
Note: Skip ahead to the Setup Instructions section [Setup Instructions](#setup-instructions) for a quick walkthrough of the demo setup.

Note : Jump to [Setup Instructions](#setup-instructions) for quickly goung through the demo
----
## Overview

This project implements an Inventory Management system with two components:

1. **Inventory Service**: A REST API managing inventory counts of `tshirts` and `pants`.
2. **MCP Server (Model Control Plane)**: A GenAI-powered interface that interprets natural language commands to interact with the Inventory Service.

----
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
├── start_all.bat                       # Bonus: Script to run all components in new terminal tabs (WINDOWS)
├── start_all.sh                        # Bonus: Script to run all components in new terminal tabs (MACOS)
├── requirements.txt                    # Dependencies of the entire system. Required If you are running start_all files directly.
└── README.md                           # Documentation and setup instructions
```
### inventory-service/
Backend REST API to manage inventory for tshirts and pants.
| File               | Description                                                                            |
| ------------------ | -------------------------------------------------------------------------------------- |
| `main.py`          | FastAPI application that exposes `GET` and `POST` endpoints for inventory.             |
| `inventory.py`     | Contains business logic to load, update, and persist inventory using `inventory.json`. |
| `models.py`        | Defines the request schema using `Pydantic` to validate `POST /inventory` input.       |
| `inventory.json`   | Stores current inventory count in JSON format. Auto-saved on updates.                  |
| `requirements.txt` | Lists all Python dependencies needed to run this service.                              |

### mcp-server/
Model Control Plane (MCP) server. Accepts natural language and interacts with the inventory API using LLM.
| File                  | Description                                                                                     |
| --------------------- | ----------------------------------------------------------------------------------------------- |
| `main.py`             | FastAPI app that parses user queries and routes them as actions (GET/POST) to the inventory.    |
| `utils.py`            | Handles OpenRouter LLM calls to convert natural language into structured JSON actions.          |
| `inventory_client.py` | Contains async HTTP functions to call the inventory service's endpoints.                        |
| `prompts.py`          | System prompt + examples used to guide the LLM in formatting responses.                         |
| `.env`                | Stores sensitive OpenRouter API key and model name (e.g., `mistral-small`). Not tracked by Git. |
| `requirements.txt`    | Lists dependencies like `fastapi`, `httpx`, `python-dotenv`, etc.                               |
### mcp-client/ (Optional CLI)
Simple command-line interface to talk to the MCP server.
| File     | Description                                                                                                  |
| -------- | ------------------------------------------------------------------------------------------------------------ |
| `cli.py` | Takes natural language input from user and sends it to MCP (`localhost:8001/mcp`) and displays the response. |

### openapi.yaml

Defines the OpenAPI spec of the inventory service. Helps LLMs understand valid endpoints and data formats.

### start_all.bat (Bonus)
Batch script to run the entire system (inventory service, MCP server, and client) with one click on Windows.

| Step | Action                                                   |
| ---- | -------------------------------------------------------- |
| 1️  | Opens inventory service in new CMD window on port `8000` |
| 2️  | Opens MCP server in new CMD window on port `8001`        |
| 3️  | Opens MCP CLI in third CMD window                        |

### start_all.sh (Bonus)
Shell script to run the entire system (inventory service, MCP server, and client) with one click on MAC OS.

| Step | Action                                                   |
| ---- | -------------------------------------------------------- |
| 1️  | Opens inventory service in new Terminal on port `8000` |
| 2️  | Opens MCP server in new Terminalon port `8001`        |
| 3️  | Opens MCP CLI in third Terminal                        |

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
This is a very crucial step and needs to be completed for the servers to run with LLM support.
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

### start_all.sh
Run all services in one go by clicking on start_all.sh (MAC OS)   

--- 
Make sure to install root/requirements.txt beforehand to ensure everything runs smoothly.    

```pip install -r requirements.txt```   

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
## Experimentation & Design Decisions
Throughout this project, I explored different approaches and made thoughtful decisions to balance functionality, simplicity, and learning. Here’s a breakdown of the key experiments, challenges, and choices I made along the way:

### 1. Tech Stack Choices
| Component       | Choice                         | Reasoning                                                                                                                                                                                |
| --------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Web Framework   | **FastAPI**                    | Chosen for its speed, automatic OpenAPI docs generation, and async support. Although Flask was considered, FastAPI provided built-in validation and better type hinting with `Pydantic`. |
| LLM Integration | **OpenRouter API**             | Selected for free-tier access to multiple models and OpenAI-compatible API.                                                                                                              |
| Data Store      | **JSON File (inventory.json)** | Used simple persistent storage via a file to avoid DB setup; enough for a small-scale system and prototyping.                                                                            |
| HTTP Client     | **httpx (async)**              | Used for making asynchronous HTTP calls between MCP server and Inventory service.                                                                                                        |
| Language Model  | **Mistral-7B via OpenRouter**  | Initial attempts with Gemma failed due to developer instruction issues; switched to a Mistral model known for better instruction-following capability.                                   |

----
### 2. Development Process & Experimentation
### Inventory Service
+ Initial Version: Started with in-memory dictionary (inventory_data).

+ Persistence Experiment: Noticed that data resets on server restart. Switched to JSON-based file persistence.

+ Improved Error Handling: Prevented negative inventory by checking for underflow.

+ OpenAPI Spec: Initially skipped, later added openapi.yaml for better integration with GenAI prompting.

+ Fallback Mechanism: If inventory.json is missing, it defaults to a hardcoded fallback.

#### MCP Server
* Prompt Parsing: Faced challenges in parsing raw LLM output (extra Markdown code blocks). Implemented stripping of triple backticks and json block markers.

* LLM Switching: Switched from gemma to mistral-small after discovering support issues and malformed outputs.

* Robust Validation: Added checks for valid keys (item, change) and data types to catch LLM hallucinations or misformats.

* Error Trace Debugging: Tracked HTTP 400s to invalid change data types (str instead of int) and refined input handling.
----
#### 3. Tooling Decisions
* Environment Variables: .env used to safely manage API keys and models.

* Batch and Shell Automation: start_all.bat and start_all.sh created to run Inventory, MCP server, and CLI in parallel for ease of testing.

* Postman Testing: Preferred over curl for better visualization and ease during JSON request testing.
----
 ### 4. Test Case Trials

| Scenario                          | Observation                           | Fix                                                |
| --------------------------------- | ------------------------------------- | -------------------------------------------------- |
| Selling more than available stock | Allowed initially, causing negatives  | Added validation to block it                       |
| Missing fields in LLM response    | Crashed server                        | Added validation for field presence and type       |
| LLM returning invalid JSON format | Caused JSON decode errors             | Added cleaning logic for Markdown code blocks      |
| No `.json` file at startup        | Inventory wiped                       | Added check to load defaults if file doesn't exist |
| Persistent storage not updating   | Was initially only saving on shutdown | Changed to write immediately after POST            |

----
 ### 5. Bonus Experiments
* CLI Client (mcp-client/cli.py): Built a simple terminal-based interactive client using input() for quick queries to MCP.

* Prompt Engineering: Customized prompts.py to support  edge cases like "show me total stock of shoes".

* OpenAPI-Aided Prompting: Used openapi.yaml to ground LLM outputs into correct schema actions.

---

## Key Learnings
+ LLMs can hallucinate or misformat responses, so always validate inputs.

+ OpenAPI docs aren’t just for Swagger—they help guide GenAI to respond in expected formats.

+ Persistent storage is crucial, even in small-scale apps, especially when testing state.

+ Developer experience matters — start_all.bat saves significant manual setup time.
---
## Conclusion
This project was a great opportunity to blend traditional backend skills with the exciting capabilities of generative AI. From designing clean APIs and managing state with file-based persistence, to integrating OpenRouter for natural language understanding — each part pushed me to think like both an engineer and a product builder.

Along the way, I explored prompt design, experimented with LLM models, and made decisions that kept the system simple, modular, and extensible.

More than just completing a task, this was about delivering something functional and demonstrating how modern AI can effectively integrate with real-world systems

Thanks for reading !
