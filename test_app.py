import unittest
import json
from app import app, get_db_connection

class StudentPerformanceMonitoringTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_students(self):
        response = self.app.get('/students')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student List', response.data)

    def test_student_profile(self):
        response = self.app.get('/student/1')
        print("Profile Response Data:", response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Htin Aung Linn', response.data)
        self.assertIn(b'Ratings', response.data)
        self.assertIn(b'Debts', response.data)

    def test_add_student(self):
        new_student = {
            'id': 38,
            'name': 'Min Thu Kyaw',
            'ratings': json.dumps({
                'Discipline 1': 85,
                'Discipline 2': 90,
                'Discipline 3': 88,
                'Discipline 4': 92,
                'Discipline 5': 87
            }),
            'debts': json.dumps(['Late submission'])
        }
        response = self.app.post('/add_student', data=new_student)
        print("Add Student Response Data:", response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'New student added successfully!', response.data)

    def test_edit_student(self):
        updated_student = {
            'name': 'Kaung Htet San',
            'ratings': json.dumps({
                'Discipline 1': 95,
                'Discipline 2': 95,
                'Discipline 3': 95,
                'Discipline 4': 95,
                'Discipline 5': 94
            }),
            'debts': json.dumps([])
        }
        response = self.app.post('/edit_student/2', data=updated_student)
        print("Edit Student Response Data:", response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student updated successfully!', response.data)

    def test_delete_student(self):
        response = self.app.post('/delete_student/37')
        print("Delete Student Response Data:", response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student deleted successfully!', response.data)

if __name__ == '__main__':
    unittest.main()
