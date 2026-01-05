import sqlite3
from werkzeug.security import generate_password_hash

# Connect to the database
conn = sqlite3.connect('project.db')
cursor = conn.cursor()

# Create a new user with a known password
email = 'test@example.com'
name = 'Test User'
password = 'test123'
password_hash = generate_password_hash(password)

try:
    cursor.execute(
        'INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)',
        (email, name, password_hash)
    )
    conn.commit()
    print(f"Created user {email} with password {password}")
except sqlite3.IntegrityError:
    print(f"User {email} already exists")
    # Update the password instead
    cursor.execute(
        'UPDATE users SET password_hash = ? WHERE email = ?',
        (password_hash, email)
    )
    conn.commit()
    print(f"Updated password for user {email}")

conn.close()