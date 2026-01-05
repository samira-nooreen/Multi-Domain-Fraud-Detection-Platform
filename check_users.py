import sqlite3

# Connect to the database
conn = sqlite3.connect('project.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=== Users Table ===")
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

if users:
    for user in users:
        print(f"ID: {user['id']}, Email: {user['email']}, Name: {user['name']}")
else:
    print("No users found")

conn.close()