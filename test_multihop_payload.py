import requests
import json

url = "http://127.0.0.1:8000/evaluate/"

payload = {
    "entity_reference": "ENT-MULTIHOP-001",
    "metrics": [
        {
            "pillar_name": "Transaction Velocity",
            "metric_score": 65.0,
            "details": "Moderate velocity spike across intermediate proxy nodes"
        },
        {
            "pillar_name": "Network Risk",
            "metric_score": 90.0,
            "details": "High structural clustering coefficient; linked to 3 flagged syndication wallets"
        }
    ]
}

headers = {"Content-Type": "application/json"}

if __name__ == "__main__":
    try:
        print(f"Sending multi-hop stress payload for {payload['entity_reference']}...")
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(json.dumps(response.json(), indent=4))
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the FastAPI server.")
