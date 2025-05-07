from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
# Create your tests here.


class LogitTestCase(TestCase):
    """Test login function"""

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='hello', password='password123')
    
    def test_login_user(self):
        response = self.client.post(
            reverse('user:login'),
            data={'username': 'hello', 'password': 'password123'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'), target_status_code=200)

    def test_login_wrong_user(self):
        response = self.client.post(
            reverse('user:login'),
            data={'username': 'hello', 'password': 'password'}
        )
        messages = list(get_messages(response.wsgi_request))
        text = "Username or password is incorrect"
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(messages[0]), text)
    