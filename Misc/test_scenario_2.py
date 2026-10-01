import requests
import json

url = "http://127.0.0.1:8000/evaluate/"
payload = {
    "entity_reference": "ENT-COMPLEX-002 (Fan-In Funnel)",
    "metrics": [
        {
            "pillar_name": "Transaction Velocity",
            "metric_score": 92.0,
            "details": "Massive fan-in velocity spike; 45 micro-deposits aggregating into a single hub within 1 hour"
        },
        {
            "pillar_name": "Network Risk",
            "metric_score": 88.0,
            "details": "High indegree centrality linking to multiple newly created sleeper wallets"
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
