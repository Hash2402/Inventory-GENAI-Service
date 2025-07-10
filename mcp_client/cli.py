import requests

def main():
    print("Welcome to the Inventory Assistant!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("User: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = requests.post(
            "http://localhost:8001/mcp",  # MCP server
            json={"message": user_input}
        )

        if response.status_code == 200:
            data = response.json()
            print(" Action:", data.get("action"))
            print(" Inventory:", data.get("response"))
        else:
            print(" Error:", response.json().get("detail"))

if __name__ == "__main__":
    main()
