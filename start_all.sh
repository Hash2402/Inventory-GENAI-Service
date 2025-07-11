#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Starting AI Inventory Services..."
echo "Script directory: $SCRIPT_DIR"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if required commands exist
if ! command_exists uvicorn; then
    echo "Error: uvicorn is not installed. Please install it with: pip install uvicorn"
    exit 1
fi

# Check for Python (prefer python3 on Mac)
PYTHON_CMD=""
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
else
    echo "Error: Neither python3 nor python is installed or not in PATH"
    exit 1
fi

echo "Using Python command: $PYTHON_CMD"

# Function to cleanup background processes on script exit
cleanup() {
    echo "Stopping services..."
    if [ ! -z "$INVENTORY_PID" ]; then
        kill $INVENTORY_PID 2>/dev/null
    fi
    if [ ! -z "$MCP_SERVER_PID" ]; then
        kill $MCP_SERVER_PID 2>/dev/null
    fi
    echo "Note: MCP client is running in a separate terminal window - close it manually if needed"
    exit 0
}

# Set up signal handlers for cleanup
trap cleanup SIGINT SIGTERM

# Start inventory service
echo "Starting inventory service on port 8000..."
cd inventory-service
uvicorn main:app --port 8000 --reload &
INVENTORY_PID=$!
cd ..

# Start MCP server
echo "Starting MCP server on port 8001..."
cd mcp-server
uvicorn main:app --port 8001 --reload &
MCP_SERVER_PID=$!
cd ..

# Wait for services to start
echo "Waiting for services to start..."
sleep 2

# Start MCP client in new terminal window
echo "Starting MCP client in new terminal window..."
osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR/mcp_client' && $PYTHON_CMD cli.py\""

echo "All services started successfully!"
echo "- Inventory Service: http://localhost:8000"
echo "- MCP Server: http://localhost:8001"
echo "- MCP Client: Running in new terminal window"
echo ""
echo "Press Ctrl+C to stop the backend services"
echo "Close the MCP client terminal window manually when done"

# Wait for all background processes
wait 