import requests

def main():
    print("Welcome to the Inventory Assistant!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("User: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Send user's message to MCP server for processing
        response = requests.post(
            "http://localhost:8001/mcp",  # MCP server URL
            json={"message": user_input}
        )

        if response.status_code == 200:
            data = response.json()
            # Print the action MCP interpreted and the inventory state
            print(" Action:", data.get("action"))
            print(" Inventory:", data.get("response"))
        else:
            # Print error message if MCP server returns error
            print(" Error:", response.json().get("detail"))

if __name__ == "__main__":
    main()
