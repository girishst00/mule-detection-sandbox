def detect_circular_layering():
    transactions = [
        {'tx_id': 'T1', 'from': 'EXT_SOURCE', 'to': 'MULE_PRIMARY', 'amount': 100000},
        {'tx_id': 'T2', 'from': 'MULE_PRIMARY', 'to': 'SUB_MULE_A', 'amount': 50000},
        {'tx_id': 'T3', 'from': 'MULE_PRIMARY', 'to': 'SUB_MULE_B', 'amount': 49000},
        {'tx_id': 'T4', 'from': 'SUB_MULE_A', 'to': 'AGGREGATOR', 'amount': 49500},
        {'tx_id': 'T5', 'from': 'SUB_MULE_B', 'to': 'AGGREGATOR', 'amount': 48500},
    ]
    print('--- Running Circular Layering / Fan-Out Check ---')
    inflow = sum(t['amount'] for t in transactions if t['to'] == 'MULE_PRIMARY')
    outflow = sum(t['amount'] for t in transactions if t['from'] == 'MULE_PRIMARY')
    print(f'Primary Mule Inflow: {inflow}')
    print(f'Primary Mule Outflow: {outflow}')
    
    if outflow >= (inflow * 0.80):
        print('\n[!] ALERT: Circular Layering / Fan-Out Pattern Detected on MULE_PRIMARY!')
    else:
        print('\n[+] Behavior looks normal.')

if __name__ == '__main__':
    detect_circular_layering()

