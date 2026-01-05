"""
Demo Script for Fraud Detection Database Integration
This script demonstrates the database integration features.
"""

import sqlite3
import json
from datetime import datetime

def demo_database_queries():
    """Demonstrate database queries for fraud analysis logs"""
    print("🔍 Fraud Detection Database Integration - Demo")
    print("=" * 50)
    
    # Connect to the database
    conn = sqlite3.connect('project.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n📊 Database Schema Overview:")
    print("-" * 30)
    
    # Show all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Tables in database:")
    for table in tables:
        print(f"  • {table[0]}")
    
    print("\n📋 Sample Data from fraud_analysis_logs:")
    print("-" * 40)
    
    # Show table structure
    cursor.execute("PRAGMA table_info(fraud_analysis_logs)")
    columns = cursor.fetchall()
    print("Columns in fraud_analysis_logs:")
    for col in columns:
        print(f"  • {col[1]} ({col[2]})")
    
    # Show sample records (if any)
    cursor.execute("SELECT COUNT(*) FROM fraud_analysis_logs")
    count = cursor.fetchone()[0]
    print(f"\nTotal fraud analysis logs: {count}")
    
    if count > 0:
        print("\nRecent fraud analysis logs:")
        cursor.execute("""
            SELECT id, user_id, module_name, fraud_probability, risk_level, timestamp 
            FROM fraud_analysis_logs 
            ORDER BY timestamp DESC 
            LIMIT 5
        """)
        records = cursor.fetchall()
        for record in records:
            print(f"  ID: {record['id']}, User: {record['user_id']}, Module: {record['module_name']}")
            print(f"    Probability: {record['fraud_probability']:.2f}, Risk: {record['risk_level']}")
            print(f"    Time: {record['timestamp']}")
            print()
    else:
        print("No fraud analysis logs found yet.")
        print("Run some fraud detection analyses to populate this table!")
    
    print("\n📈 Analytics Data Summary:")
    print("-" * 25)
    
    # Show analytics data summary
    cursor.execute("SELECT COUNT(*) FROM analytics_data")
    count = cursor.fetchone()[0]
    print(f"Total analytics records: {count}")
    
    if count > 0:
        cursor.execute("""
            SELECT category, COUNT(*) as count, AVG(value) as average
            FROM analytics_data 
            GROUP BY category
        """)
        analytics = cursor.fetchall()
        print("\nAnalytics by category:")
        for item in analytics:
            print(f"  • {item['category']}: {item['count']} records (avg: {item['average']:.2f})")
    else:
        print("No analytics data found yet.")
    
    conn.close()
    
    print("\n💡 How to Generate Data:")
    print("-" * 25)
    print("1. Run the Flask application: python app.py")
    print("2. Log in to the web interface")
    print("3. Use any fraud detection module")
    print("4. Visit the Analytics Dashboard")
    print("5. Run this script again to see the data!")

def demo_sql_queries():
    """Show useful SQL queries for exploring the database"""
    print("\n🔍 Useful SQL Queries:")
    print("=" * 25)
    
    queries = [
        ("View all fraud analysis logs", "SELECT * FROM fraud_analysis_logs;"),
        ("Count analyses by module", "SELECT module_name, COUNT(*) as count FROM fraud_analysis_logs GROUP BY module_name;"),
        ("Recent high-risk detections", "SELECT * FROM fraud_analysis_logs WHERE risk_level IN ('HIGH', 'CRITICAL') ORDER BY timestamp DESC LIMIT 10;"),
        ("Average fraud probability by module", "SELECT module_name, AVG(fraud_probability) as avg_prob FROM fraud_analysis_logs GROUP BY module_name;"),
        ("User activity summary", "SELECT user_id, COUNT(*) as analyses, MAX(timestamp) as last_activity FROM fraud_analysis_logs GROUP BY user_id;"),
        ("Analytics data overview", "SELECT category, COUNT(*) as count, AVG(value) as average FROM analytics_data GROUP BY category;")
    ]
    
    for description, query in queries:
        print(f"\n{description}:")
        print(f"```sql\n{query}\n```")

if __name__ == "__main__":
    demo_database_queries()
    demo_sql_queries()
    
    print("\n" + "=" * 50)
    print("✨ Database integration demo complete!")
    print("The fraud detection platform now stores all analyses")
    print("persistently and provides real-time analytics.")