from flask import Flask, jsonify, request, render_template, render_template_string
import sqlite3
import json

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('students.db', timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def get_student_info(student):
    conn = get_db_connection()
    student_info = dict(student)
    ratings = conn.execute('SELECT discipline, rating FROM Ratings WHERE student_id = ?', (student['id'],)).fetchall()
    student_info['ratings'] = {rating['discipline']: rating['rating'] for rating in ratings}
    debts = conn.execute('SELECT debt FROM Debts WHERE student_id = ?', (student['id'],)).fetchall()
    student_info['debts'] = [debt['debt'] for debt in debts]
    conn.close()
    return student_info

@app.route('/students', methods=['GET'])
def get_students():
    with get_db_connection() as conn:
        students = conn.execute('SELECT * FROM Students').fetchall()
        students_list = [get_student_info(student) for student in students]
    return render_template('students.html', students=students_list)

@app.route('/search', methods=['GET'])
def search_students():
    query = request.args.get('query')
    rating_filter = request.args.get('rating_filter')
    rating_threshold = request.args.get('rating_threshold')
    search_results = []
    
    with get_db_connection() as conn:
        if query:
            if query.isdigit():
                student = conn.execute('SELECT * FROM Students WHERE id = ?', (query,)).fetchall()
                search_results.extend([get_student_info(s) for s in student])
            else:
                query = f"%{query}%"
                students = conn.execute('SELECT * FROM Students WHERE name LIKE ?', (query,)).fetchall()
                search_results.extend([get_student_info(s) for s in students])
                
        if rating_filter and rating_threshold:
            rating_threshold = float(rating_threshold)
            if rating_filter == 'above':
                ratings = conn.execute('SELECT student_id FROM Ratings WHERE rating > ?', (rating_threshold,)).fetchall()
            else:
                ratings = conn.execute('SELECT student_id FROM Ratings WHERE rating < ?', (rating_threshold,)).fetchall()
                
            student_ids = [r['student_id'] for r in ratings]
            if student_ids:
                students = conn.execute(f'SELECT * FROM Students WHERE id IN ({",".join("?"*len(student_ids))})', student_ids).fetchall()
                search_results.extend([get_student_info(s) for s in students])
    return render_template('students.html', students=search_results)

@app.route('/student/<int:student_id>', methods=['GET'])
def student_profile(student_id):
    with get_db_connection() as conn:
        student = conn.execute('SELECT * FROM Students WHERE id = ?', (student_id,)).fetchone()
        if student is None:
            return "Student not found", 404

        student_info = get_student_info(student)

    return render_template('student_profile.html', student=student_info)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            new_student = request.form.to_dict()
            new_student['ratings'] = json.loads(new_student['ratings'])
            new_student['debts'] = json.loads(new_student['debts'])

            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO Students (id, name) VALUES (?, ?)', (new_student['id'], new_student['name']))

                for discipline, rating in new_student['ratings'].items():
                    cursor.execute('INSERT INTO Ratings (student_id, discipline, rating) VALUES (?, ?, ?)', (new_student['id'], discipline, rating))

                for debt in new_student['debts']:
                    cursor.execute('INSERT INTO Debts (student_id, debt) VALUES (?, ?)', (new_student['id'], debt))

                conn.commit()
            return "New student added successfully!", 201
        except json.JSONDecodeError as e:
            return f"Invalid JSON format: {e}", 400
        except Exception as e:
            return f"An error occurred: {e}", 400

    return render_template_string('''
    <form method="post">
        ID: <input type="text" name="id"><br>
        Name: <input type="text" name="name"><br>
        Ratings (JSON format): <textarea name="ratings">{"Discipline 1": 90, "Discipline 2": 85, "Discipline 3": 80, "Discipline 4": 95, "Discipline 5": 88}</textarea><br>
        Debts (JSON format): <textarea name="debts">[]</textarea><br>
        <input type="submit">
    </form>
    ''')

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    with get_db_connection() as conn:
        student = conn.execute('SELECT * FROM Students WHERE id = ?', (student_id,)).fetchone()
        if student is None:
            return "Student not found", 404

        if request.method == 'POST':
            try:
                updated_student = request.form.to_dict()
                updated_student['ratings'] = json.loads(updated_student['ratings'])
                updated_student['debts'] = json.loads(updated_student['debts'])

                cursor = conn.cursor()

                print("Update Student Params:", (updated_student['name'], student_id))
                cursor.execute('UPDATE Students SET name = ? WHERE id = ?', (updated_student['name'], student_id))

                print("Delete Ratings Params:", (student_id,))
                cursor.execute('DELETE FROM Ratings WHERE student_id = ?', (student_id,))
                for discipline, rating in updated_student['ratings'].items():
                    print("Insert Ratings Params:", (student_id, discipline, rating))
                    cursor.execute('INSERT INTO Ratings (student_id, discipline, rating) VALUES (?, ?, ?)', (student_id, discipline, rating))

                print("Delete Debts Params:", (student_id,))
                cursor.execute('DELETE FROM Debts WHERE student_id = ?', (student_id,))
                for debt in updated_student['debts']:
                    print("Insert Debts Params:", (student_id, debt))
                    cursor.execute('INSERT INTO Debts (student_id, debt) VALUES (?, ?)', (student_id, debt))

                conn.commit()
                return "Student updated successfully!", 200
            except json.JSONDecodeError as e:
                return f"Invalid JSON format: {e}", 400
            except Exception as e:
                return f"An error occurred: {e}", 400

        student_info = get_student_info(student)

    return render_template_string('''
    <form method="post">
        Name: <input type="text" name="name" value="{{ name }}"><br>
        Ratings (JSON format): <textarea name="ratings">{"Discipline 1": 90, "Discipline 2": 85, "Discipline 3": 80, "Discipline 4": 95, "Discipline 5": 88}</textarea><br>
        Debts (JSON format): <textarea name="debts">{{ debts }}</textarea><br>
        <input type="submit">
    </form>
    ''', **student_info)


@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    with get_db_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Students WHERE id = ?', (student_id,))
            cursor.execute('DELETE FROM Ratings WHERE student_id = ?', (student_id,))
            cursor.execute('DELETE FROM Debts WHERE student_id = ?', (student_id,))

            conn.commit()
            return "Student deleted successfully!", 200
        except Exception as e:
            return f"An error occurred: {e}", 400

if __name__ == '__main__':
    app.run(debug=True)
