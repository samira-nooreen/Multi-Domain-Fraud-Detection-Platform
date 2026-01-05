import sqlite3
import json

def export_database_info():
    """Export database structure and sample data"""
    
    # Connect to the database
    conn = sqlite3.connect('project.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("SQLite Database: project.db")
    print("=" * 50)
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    # Process each table
    for table in tables:
        table_name = table[0]
        if table_name == 'sqlite_sequence':
            continue  # Skip internal SQLite table
            
        print(f"\nTable: {table_name}")
        print("-" * 30)
        
        # Get column info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print("Columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"Row count: {count}")
        
        # Show sample data if available
        if count > 0:
            print("\nSample data (first 3 rows):")
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            rows = cursor.fetchall()
            
            for i, row in enumerate(rows, 1):
                print(f"  Row {i}:")
                for col in columns:
                    col_name = col[1]
                    value = row[col_name]
                    if value is None:
                        print(f"    {col_name}: NULL")
                    elif isinstance(value, str) and len(value) > 100:
                        print(f"    {col_name}: {value[:100]}...")
                    else:
                        print(f"    {col_name}: {value}")
                print()
    
    conn.close()

if __name__ == "__main__":
    export_database_info()