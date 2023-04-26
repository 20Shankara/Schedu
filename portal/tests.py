from django.test import TestCase, Client
from django.contrib.auth.models import User
from portal.models import *

class status_code_tests(TestCase):

    def create_user(self, is_active=True):
        user = User.objects.create(username="test", email="test@test.com")
        user.set_password('test')
        user.save()
        student = Student.objects.create(
            student_first_name='test',
            student_last_name='test',
            student_email="test@test.com",
            year_in_school='3',
        )
        student.save()
        return user

    def login(self):
        user = self.create_user()
        client = Client()
        client.login(username='test', password='test')
        return client

    # Student Tests
    def test_student(self):
        client = Client()
        response = client.get('/student_sign_up')
        self.assertEqual(response.status_code, 200)

    def test_class_lookup(self):
        client = self.login()
        response = client.get('/class_search')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    # Advisor Tests
    def test_advisor(self):
        client = Client()
        response = client.get('/advisor_sign_up')
        self.assertEqual(response.status_code, 200)
