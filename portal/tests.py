from django.test import TestCase, Client

class status_code_tests(TestCase):
    def test_advisor(self):
        client = Client()
        response = client.get('/advisor_sign_up')
        self.assertEqual(response.status_code, 200)

    def test_student(self):
        client = Client()
        response = client.get('/student_sign_up')
        self.assertEqual(response.status_code, 200)