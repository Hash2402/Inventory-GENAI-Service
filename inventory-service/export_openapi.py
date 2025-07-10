import requests
import yaml

def export_openapi_yaml(url="http://localhost:8000/openapi.json", filename="openapi.yaml"):
    response = requests.get(url)
    response.raise_for_status()
    openapi_json = response.json()
    with open(filename, "w") as f:
        yaml.dump(openapi_json, f, sort_keys=False)
    print(f"OpenAPI spec saved to {filename}")

if __name__ == "__main__":
    export_openapi_yaml()
