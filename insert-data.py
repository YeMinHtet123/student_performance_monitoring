import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('students.db')

# Create a cursor object
cursor = conn.cursor()

# Insert sample data into Students table
students = [
    (1, 'Htin Aung Linn'),
    (2, 'Kaung Htet San'),
    (3, 'Thtet Naing Linn'),
    (4, 'Thet Htoo Aung'),
    (5, 'Arker Min')
]

cursor.executemany('INSERT INTO Students (id, name) VALUES (?, ?)', students)

# Insert sample data into Ratings table
ratings = [
    (1, 1, 'Discipline 1', 100),
    (2, 1, 'Discipline 2', 100),
    (3, 1, 'Discipline 3', 100),
    (4, 1, 'Discipline 4', 100),
    (5, 1, 'Discipline 5', 100),
    (6, 2, 'Discipline 1', 95),
    (7, 2, 'Discipline 2', 95),
    (8, 2, 'Discipline 3', 95),
    (9, 2, 'Discipline 4', 95),
    (10, 2, 'Discipline 5', 95),
    (11, 3, 'Discipline 1', 94),
    (12, 3, 'Discipline 2', 94),
    (13, 3, 'Discipline 3', 94),
    (14, 3, 'Discipline 4', 94),
    (15, 3, 'Discipline 5', 94),
    (16, 4, 'Discipline 1', 93),
    (17, 4, 'Discipline 2', 93),
    (18, 4, 'Discipline 3', 93),
    (19, 4, 'Discipline 4', 93),
    (20, 4, 'Discipline 5', 93),
    (21, 5, 'Discipline 1', 92),
    (22, 5, 'Discipline 2', 92),
    (23, 5, 'Discipline 3', 92),
    (24, 5, 'Discipline 4', 92),
    (25, 5, 'Discipline 5', 92)
]

cursor.executemany('INSERT INTO Ratings (id, student_id, discipline, rating) VALUES (?, ?, ?, ?)', ratings)

# Insert sample data into Debts table
debts = []

cursor.executemany('INSERT INTO Debts (id, student_id, debt) VALUES (?, ?, ?)', debts)

# Commit changes and close connection
conn.commit()
conn.close()
