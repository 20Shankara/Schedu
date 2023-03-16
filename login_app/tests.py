from django.test import TestCase, Client

class StatusCodeTests(TestCase):
    def test_login_page_status(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_advisor_sign_up(self):
        client = Client()
        response = client.get('/advisorSignUp')
        self.assertEqual(response.status_code, 200)

    def test_student_sign_up(self):
        client = Client()
        response = client.get('/studentSignUp')
        self.assertEqual(response.status_code, 200)