import requests
import json

url = "http://127.0.0.1:8000/evaluate/"
payload = {
    "entity_reference": "ENT-COMPLEX-001 (Ouroboros Ring)",
    "metrics": [
        {
            "pillar_name": "Transaction Velocity",
            "metric_score": 80.0,
            "details": "Rapid consecutive fund transfers executed across 4 nodes within a 10-minute window"
        },
        {
            "pillar_name": "Network Risk",
            "metric_score": 95.0,
            "details": "Closed cyclic loop detected; high structural clustering coefficient indicating synthetic layering ring"
        }
    ]
}
headers = {"Content-Type": "application/json"}

if __name__ == "__main__":
    print(f"Evaluating -> {payload['entity_reference']}...")
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(json.dumps(response.json(), indent=4))
