import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('students.db')

# Create a cursor object
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Ratings (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    discipline TEXT,
    rating REAL,
    FOREIGN KEY(student_id) REFERENCES Students(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Debts (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    debt TEXT,
    FOREIGN KEY(student_id) REFERENCES Students(id)
)
''')

# Commit changes and close connection
conn.commit()
conn.close()
