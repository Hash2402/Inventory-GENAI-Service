start cmd /k "cd inventory-service && uvicorn main:app --port 8000 --reload"
start cmd /k "cd mcp-server && uvicorn main:app --port 8001 --reload"
timeout /t 2
start cmd /k "cd mcp-client && python cli.py"
