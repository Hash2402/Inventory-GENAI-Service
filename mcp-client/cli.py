import requests

def format_inventory(inv: dict) -> str:
    """Return a human‑readable string from the inventory dict."""
    shirts = inv.get("tshirts", "‑")
    pants  = inv.get("pants",  "‑")
    return f"{shirts} t‑shirts and {pants} pants"

def main():
    print("Welcome to the Inventory Assistant!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("User: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = requests.post(
            "http://localhost:8001/mcp",
            json={"message": user_input}
        )

        if response.status_code == 200:
            data = response.json()
            action = data.get("action")
            inventory = data.get("response", {})

            if action == "GET":
                print("Assistant: Here’s your current stock →", format_inventory(inventory))
            elif action == "POST":
                print("Assistant: Update successful! New inventory →", format_inventory(inventory))
            else:
                # Fallback if MCP ever returns a different action
                print("Assistant:", data)
        else:
            print("Assistant (error):", response.json().get("detail"))

if __name__ == "__main__":
    main()
