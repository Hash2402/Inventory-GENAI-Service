#!/bin/bash

# Get the directory of this script
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Start inventory-service in new Terminal tab
osascript -e "tell application \"Terminal\" to do script \"cd '$ROOT_DIR/inventory-service' && uvicorn main:app --reload --port 8000\""

# Start mcp-server in new Terminal tab
osascript -e "tell application \"Terminal\" to do script \"cd '$ROOT_DIR/mcp-server' && uvicorn main:app --reload --port 8001\""

# Wait for servers to start
sleep 2

# Start mcp-client in new Terminal tab
osascript -e "tell application \"Terminal\" to do script \"cd '$ROOT_DIR/mcp-client' && python cli.py\""
