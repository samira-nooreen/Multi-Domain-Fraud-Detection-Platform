import sqlite3
import json

def view_database():
    """Display all tables and their contents in the database"""
    # Connect to the database
    conn = sqlite3.connect('project.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("=" * 60)
    print("DATABASE CONTENT VIEWER")
    print("=" * 60)
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"\nFound {len(tables)} tables in the database:")
    for table in tables:
        if table[0] != 'sqlite_sequence':  # Skip internal SQLite table
            print(f"  - {table[0]}")
    
    # Display contents of each table
    for table in tables:
        table_name = table[0]
        if table_name == 'sqlite_sequence':
            continue  # Skip internal SQLite table
            
        print(f"\n{'='*20} {table_name.upper()} TABLE {'='*20}")
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        print("Columns:", ", ".join(column_names))
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"Total rows: {count}")
        
        if count > 0:
            # Display sample rows (up to 10)
            limit = min(count, 10)
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
            rows = cursor.fetchall()
            
            print(f"\nFirst {limit} rows:")
            print("-" * 40)
            for i, row in enumerate(rows, 1):
                print(f"Row {i}:")
                for col_name in column_names:
                    value = row[col_name]
                    # Try to pretty-print JSON data
                    if isinstance(value, str):
                        if value.startswith('{') or value.startswith('['):
                            try:
                                parsed = json.loads(value)
                                print(f"  {col_name}: {json.dumps(parsed, indent=2)}")
                            except:
                                print(f"  {col_name}: {value}")
                        else:
                            print(f"  {col_name}: {value}")
                    else:
                        print(f"  {col_name}: {value}")
                print()
        else:
            print("Table is empty.")
    
    conn.close()

if __name__ == "__main__":
    view_database()