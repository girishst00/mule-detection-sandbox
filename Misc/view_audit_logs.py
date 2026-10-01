import sqlite3

def view_logs(db_name='sandbox.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, test_id, typology, account_id, risk_score, alert_status, timestamp FROM audit_logs')
    rows = cursor.fetchall()
    
    print('--- Persistent SQLite Audit Logs ---')
    if not rows:
        print('No logs found in database.')
    for row in rows:
        print(f'ID: {row[0]} | Test: {row[1]} | Typology: {row[2]} | Account: {row[3]} | Risk Score: {row[4]}% | Status: {row[5]} | Time: {row[6]}')
        
    conn.close()

if __name__ == '__main__':
    view_logs()

