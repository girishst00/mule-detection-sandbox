import requests
import json

url = "http://127.0.0.1:8000/evaluate/"
payload = {
    "entity_reference": "ENT-COMPLEX-003 (Shell Chain)",
    "metrics": [
        {
            "pillar_name": "Transaction Velocity",
            "metric_score": 50.0,
            "details": "Deliberately paced intermediary transfers designed to mimic standard retail cadence"
        },
        {
            "pillar_name": "Network Risk",
            "metric_score": 96.0,
            "details": "Linear shell chain topology with zero historical merchant interaction or organic balance retention"
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
