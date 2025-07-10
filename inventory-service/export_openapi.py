import requests
import yaml

# URL of the running FastAPI Inventory Service's OpenAPI spec
OPENAPI_URL = "http://localhost:8000/openapi.json"

# Path where the YAML version will be saved
OUTPUT_FILE = "openapi.yaml"

def export_openapi_spec():
    try:
        # Fetch OpenAPI JSON from the running server
        response = requests.get(OPENAPI_URL)
        response.raise_for_status()  # Raise exception if request failed

        # Parse the JSON response
        openapi_json = response.json()

        # Convert to YAML format
        openapi_yaml = yaml.dump(openapi_json, sort_keys=False)

        # Write to file
        with open(OUTPUT_FILE, "w") as f:
            f.write(openapi_yaml)

        print(f"OpenAPI spec exported to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Failed to export OpenAPI spec: {e}")

# Run the function when script is executed
if __name__ == "__main__":
    export_openapi_spec()
