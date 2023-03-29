from django.test import TestCase, Client

class status_code_tests(TestCase):
    def test_login_page_status(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
