# Inventory Management + GenAI Interface

## Overview

This project implements an Inventory Management system with two components:

1. **Inventory Service**: A REST API managing inventory counts of `tshirts` and `pants`.
2. **MCP Server (Model Control Plane)**: A GenAI-powered interface that interprets natural language commands to interact with the Inventory Service.

---

## Project Structure

root/
├── inventory-service/
│ ├── main.py # FastAPI app for inventory management
│ ├── inventory.py # Business logic and JSON persistence
│ ├── models.py # Pydantic model for request validation
│ ├── inventory.json # Persistent data file
│ └── requirements.txt # Dependencies
├── mcp-server/
│ ├── main.py # MCP FastAPI server using LLM to interpret natural language
│ ├── utils.py # LLM call logic (OpenRouter integration)
│ ├── inventory_client.py # Handles calling Inventory API
│ ├── prompts.py # System instructions for the LLM
│ ├── .env # Stores OpenRouter API key and model
│ └── requirements.txt # Dependencies
├── mcp-client/
│ └── cli.py # CLI client to interact with MCP (Bonus)
├── openapi.yaml # OpenAPI spec used to guide LLM prompting
├── start_all.bat # script to run all components (Bonus)
└── README.md

---

## 🚀 Setup Instructions

### 🔧 Prerequisites

- Python 3.9+
- Recommended: create a virtual environment

---

### 📁 1. Inventory Service

#### ➤ Navigate to folder:

cd inventory-service

#### ➤ Install dependencies:

pip install -r requirements.txt

➤ Run the service:
uvicorn main:app --reload --port 8000

Data is auto-loaded from inventory.json if it exists.

After every change, the updated inventory is saved.

Swagger/OpenAPI docs: http://localhost:8000/docs
