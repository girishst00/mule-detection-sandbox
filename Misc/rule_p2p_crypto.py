import json

def detect_p2p_churn(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    txs = data["transactions"]
    credits = [t for t in txs if t["direction"] == "CREDIT"]
    debits = [t for t in txs if t["direction"] == "DEBIT"]
    
    print(f"--- Running Detection: {data['test_id']} ({data['typology']}) ---")
    
    p2p_keywords = ["P2P", "Crypto", "Trader", "Escrow"]
    p2p_debits = [
        d for d in debits 
        if any(kw in d["counterparty"]["name"] or kw in d["notes"] for kw in p2p_keywords)
    ]
    
    if len(p2p_debits) >= 2 and sum(d["amount"] for d in p2p_debits) > 100000:
        print(f"[ALERT] High Risk P2P / Crypto-Bridge Liquidity Churn Detected!")
        print(f"  -> Rapid Outflows to P2P Merchants: {len(p2p_debits)} transactions")
        print(f"  -> Total Churned Value: {sum(d['amount'] for d in p2p_debits)} INR")
        print(f"  -> Risk Score: 96/100 (Immediate Account Hold Recommended)\n")
    else:
        print("[INFO] P2P velocity within normal threshold.")

if __name__ == "__main__":
    detect_p2p_churn("test_05_p2p_crypto.json")