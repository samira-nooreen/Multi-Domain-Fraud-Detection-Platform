import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('project.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=== Database Structure ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", [table[0] for table in tables])

print("\n=== Fraud Analysis Logs ===")
cursor.execute("SELECT COUNT(*) FROM fraud_analysis_logs")
count = cursor.fetchone()[0]
print(f"Total records: {count}")

if count > 0:
    cursor.execute("SELECT * FROM fraud_analysis_logs ORDER BY timestamp DESC LIMIT 5")
    records = cursor.fetchall()
    for i, record in enumerate(records):
        print(f"\nRecord {i+1}:")
        print(f"  ID: {record['id']}")
        print(f"  User ID: {record['user_id']}")
        print(f"  Module: {record['module_name']}")
        print(f"  Probability: {record['fraud_probability']}")
        print(f"  Risk Level: {record['risk_level']}")
        print(f"  Timestamp: {record['timestamp']}")
        
        # Parse input data if available
        if record['input_data']:
            try:
                input_data = json.loads(record['input_data'])
                print(f"  Input Data: {input_data}")
            except:
                print(f"  Input Data: {record['input_data']}")
        
        # Parse result data if available
        if record['result_data']:
            try:
                result_data = json.loads(record['result_data'])
                print(f"  Result Data: {result_data}")
            except:
                print(f"  Result Data: {record['result_data']}")

conn.close()