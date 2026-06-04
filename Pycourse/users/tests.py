from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='pass1234', role='student')
    def test_login_page(self):
        r = self.client.get(reverse('login'))
        self.assertEqual(r.status_code, 200)
    def test_login_success(self):
        r = self.client.post(reverse('login'), {'username':'test','password':'pass1234'})
        self.assertRedirects(r, reverse('dashboard'))
