import sqlite3
from datetime import datetime

def log_to_database(account_id, risk_score, alert_status, db_name='sandbox.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id TEXT,
            typology TEXT,
            account_id TEXT,
            risk_score REAL,
            alert_status TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO audit_logs (test_id, typology, account_id, risk_score, alert_status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('TEST_07', 'Circular Layering & Fan-Out', account_id, risk_score, alert_status, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def detect_circular_layering():
    transactions = [
        {'tx_id': 'T1', 'from': 'EXT_SOURCE', 'to': 'MULE_PRIMARY', 'amount': 100000},
        {'tx_id': 'T2', 'from': 'MULE_PRIMARY', 'to': 'SUB_MULE_A', 'amount': 50000},
        {'tx_id': 'T3', 'from': 'MULE_PRIMARY', 'to': 'SUB_MULE_B', 'amount': 49000},
        {'tx_id': 'T4', 'from': 'SUB_MULE_A', 'to': 'AGGREGATOR', 'amount': 49500},
        {'tx_id': 'T5', 'from': 'SUB_MULE_B', 'to': 'AGGREGATOR', 'amount': 48500},
    ]
    print('--- Running Circular Layering / Fan-Out Check & Database Logging ---')
    inflow = sum(t['amount'] for t in transactions if t['to'] == 'MULE_PRIMARY')
    outflow = sum(t['amount'] for t in transactions if t['from'] == 'MULE_PRIMARY')
    
    risk_score = round((outflow / inflow) * 100, 2) if inflow > 0 else 0.0
    print(f'Primary Mule Inflow: {inflow}')
    print(f'Primary Mule Outflow: {outflow}')
    print(f'Calculated Risk Score: {risk_score}%')

    if outflow >= (inflow * 0.80):
        print('\n[!] ALERT: Circular Layering / Fan-Out Pattern Detected on MULE_PRIMARY!')
        log_to_database('MULE_PRIMARY', risk_score, 'FLAGGED_ALERT')
        print('[+] Audit record successfully written to sandbox.db')
    else:
        print('\n[+] Behavior looks normal.')
        log_to_database('MULE_PRIMARY', risk_score, 'NORMAL')
        print('[+] Audit record successfully written to sandbox.db')

if __name__ == '__main__':
    detect_circular_layering()

