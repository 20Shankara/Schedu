from django.test import TestCase, Client

class StatusCodeTests(TestCase):
    def test_login_page_status(self):
        client = Client()
        response = client.get('/')
        self.assertIs(response.status_code, "200")
