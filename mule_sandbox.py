from datetime import datetime, timedelta

def generate_mock_data():
    base_time = datetime.now() - timedelta(hours=2)
    data = []
    
    # 1. Normal User (Regular shopping)
    for i in range(5):
        data.append({
            "account_id": "USER_NORMAL_01",
            "time": base_time + timedelta(minutes=i*15),
            "type": "DEBIT",
            "amount": 200 + (i * 50),
            "counterparty": "Grocery_Store"
        })
        
    # 2. Mule Account (Rapid Pass-Through pattern)
    mule_inflow = base_time + timedelta(minutes=60)
    mule_outflow = base_time + timedelta(minutes=62) # 2 minutes later!
    
    data.append({"account_id": "MULE_SUSPECT_99", "time": mule_inflow, "type": "CREDIT", "amount": 50000, "counterparty": "Source_A"})
    data.append({"account_id": "MULE_SUSPECT_99", "time": mule_outflow, "type": "DEBIT", "amount": 49500, "counterparty": "Crypto_Exchanger"})

    return data

def detect_pass_through_mules(transactions):
    # Group transactions by account manually using standard dictionaries
    accounts = {}
    for tx in transactions:
        acc = tx["account_id"]
        if acc not in accounts:
            accounts[acc] = {"credits": [], "debits": []}
        if tx["type"] == "CREDIT":
            accounts[acc]["credits"].append(tx)
        else:
            accounts[acc]["debits"].append(tx)
            
    alerts = []
    for account_id, group in accounts.items():
        credits = group["credits"]
        debits = group["debits"]
        
        if credits and debits:
            total_in = sum(c["amount"] for c in credits)
            total_out = sum(d["amount"] for d in debits)
            
            # Check if outflow is >= 90% of inflow
            if total_out >= (total_in * 0.90):
                earliest_credit = min(c["time"] for c in credits)
                latest_debit = max(d["time"] for d in debits)
                
                time_diff_mins = (latest_debit - earliest_credit).total_seconds() / 60
                
                if time_diff_mins <= 10:
                    alerts.append({
                        "account_id": account_id,
                        "risk_reason": "Rapid Pass-Through detected",
                        "time_window_mins": round(time_diff_mins, 2),
                        "total_inflow": total_in,
                        "total_outflow": total_out
                    })
                    
    return alerts

# Execute the sandbox test
transactions = generate_mock_data()
print("--- Running Mule Detection Sandbox ---")
alerts = detect_pass_through_mules(transactions)

if alerts:
    print("\n[!] ALERTS TRIGGERED:")
    for alert in alerts:
        print(alert)
else:
    print("\n[+] No suspicious mule behavior detected.")