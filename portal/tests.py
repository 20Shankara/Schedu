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
        student.schedule = self.create_schedule()
        student.save()
        advisor = Advisor.objects.create(
            advisor_first_name='test',
            advisor_last_name='test',
            advisor_email='test@test.com',
            advisor_department='American Studies'
        )
        advisor.save()
        return user

    def create_schedule(self):
        schedule = Schedule.objects.create(
            season='8',
            classes=[],
            is_approved=False,
            is_viewed=False,
            is_sent=False,
        )
        classes = ['40', '50']
        schedule.classes = classes
        schedule.save()
        return schedule

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

    def test_student_dashboard(self):
        client = self.login()
        response = client.get('/student_dashboard')
        self.assertEqual(response.status_code, 200)

    def test_class_lookup(self):
        client = self.login()
        response = client.get('/class_search')
        self.assertEqual(response.status_code, 200)

    def test_class_results(self):
        client = self.login()
        data = {
            'department': 'CS',
            'course_num': '',
            'year': '8'
        }
        response = client.post('/results', data)
        self.assertEqual(response.status_code, 200)

    def test_class_view(self):
        client = self.login()
        data = {
            'ClassPK': '30'
        }
        response = client.post('/8/class_view', data)
        self.assertEqual(response.status_code, 200)

    def test_student_schedule(self):
        client = self.login()
        response = client.get('/student_schedule')
        self.assertEqual(response.status_code, 200)

    def test_add_class(self):
        client = self.login()
        data = {
            "Class_nbr": '14238'
        }
        response = client.post('/2/add_class', data)
        self.assertEqual(response.status_code, 302)

    def test_student_shopping_cart(self):
        client = self.login()
        response = client.get('/student_shopping_cart')
        self.assertEqual(response.status_code, 200)


    # Advisor Tests
    def test_advisor(self):
        client = Client()
        response = client.get('/advisor_sign_up')
        self.assertEqual(response.status_code, 200)

    def test_advisor_dashboard(self):
        client = self.login()
        response = client.get('/advisor_dashboard')
        self.assertEqual(response.status_code, 200)

    def test_manage_students(self):
        client = self.login()
        response = client.get('/manage_students')
        self.assertEqual(response.status_code, 200)

    def test_student_profile(self):
        client = self.login()
        data = {
            'advisee_email': 'test@test.com',
        }
        response = client.post('/student_profile', data)
        self.assertEqual(response.status_code, 200)

    def test_view_schedule(self):
        client = self.login()
        data = {
            'student_email': 'test@test.com',
        }
        response = client.post('/view_schedule', data)
        self.assertEqual(response.status_code, 200)


