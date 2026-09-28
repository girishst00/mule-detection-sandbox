import requests
import json

url = "http://127.0.0.1:8000/evaluate/"
headers = {"Content-Type": "application/json"}

scenarios = [
    {
        "entity_reference": "ENT-COMPLEX-001 (Ouroboros Ring)",
        "metrics": [
            {"pillar_name": "Transaction Velocity", "metric_score": 80.0, "details": "Rapid cyclic hops"},
            {"pillar_name": "Network Risk", "metric_score": 95.0, "details": "Closed loop clustering"}
        ]
    },
    {
        "entity_reference": "ENT-COMPLEX-002 (Fan-In Funnel)",
        "metrics": [
            {"pillar_name": "Transaction Velocity", "metric_score": 92.0, "details": "High indegree volume surge"},
            {"pillar_name": "Network Risk", "metric_score": 88.0, "details": "Sleeper wallet linkages"}
        ]
    },
    {
        "entity_reference": "ENT-COMPLEX-003 (Shell Chain)",
        "metrics": [
            {"pillar_name": "Transaction Velocity", "metric_score": 50.0, "details": "Paced structuring"},
            {"pillar_name": "Network Risk", "metric_score": 96.0, "details": "Zero organic utility chain"}
        ]
    }
]

if __name__ == "__main__":
    print("==================================================")
    print("RUNNING CONSOLIDATED MULTI-HOP BATCH EVALUATION")
    print("==================================================")
    
    for payload in scenarios:
        print(f"\nEvaluating -> {payload['entity_reference']}...")
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        res_json = response.json()
        summary = res_json.get("evaluation_summary", {})
        print(f"Composite Score: {summary.get('average_score')} | Risk Tier: {summary.get('risk_tier')}")
    
    print("\n==================================================")
    print("BATCH EVALUATION COMPLETE.")
    print("==================================================")
