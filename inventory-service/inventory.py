import json
import os

inventory_file = "inventory.json"

# Default fallback inventory
inventory_data = {
    "tshirts": 20,
    "pants": 15
}


def load_inventory():
    """
    Function to load inventory_data from the persistent inventory.json file
    """
    global inventory_data
    if os.path.exists(inventory_file):
        with open(inventory_file, "r") as f:
            inventory_data = json.load(f)
            print("Loading Inventory")
    else:
        # Create the file with default data if not present
        print("No such file, using the default inventory")
        save_inventory()


def save_inventory():
    """
    Function to save the inventory_data to the inventory.json file
    """
    with open(inventory_file, "w") as f:
        json.dump(inventory_data, f)
        print("Inventory Updated")


def get_inventory():
    """
    Simple Function to returnn the inventory_data
    """
    return inventory_data

def update_inventory(item: str, change: int):
    """
    This function validates the item to be changed as well as the value after change (Should be non-negative).
    Once validation is done change the inmemory value as well as dumps the value in the inventory.json file.
    """
    if item not in inventory_data:
        raise ValueError(f"Invalid item: '{item}' not found in inventory")

    new_quantity = inventory_data[item] + change
    if new_quantity < 0:
        raise ValueError(
            f"Cannot reduce '{item}' below 0. Current: {inventory_data[item]}, Change: {change}"
        )

    inventory_data[item] = new_quantity
    
     # Save immediately on update
    save_inventory()
    return inventory_data
