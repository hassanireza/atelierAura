from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterTest(TestCase):
    def test_register_get(self):
        r = self.client.get(reverse('register'))
        self.assertEqual(r.status_code, 200)

    def test_register_post_success(self):
        r = self.client.post(reverse('register'), {
            'first_name': 'Jane', 'last_name': 'Doe', 'username': 'janedoe',
            'email': 'jane@test.com', 'password1': 'Strongpass99!', 'password2': 'Strongpass99!'
        })
        self.assertRedirects(r, '/')
        self.assertTrue(User.objects.filter(username='janedoe').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='janedoe').exists())

    def test_register_duplicate_email(self):
        User.objects.create_user('existing', email='dupe@test.com', password='pass')
        r = self.client.post(reverse('register'), {
            'first_name': 'X', 'last_name': 'Y', 'username': 'newuser',
            'email': 'dupe@test.com', 'password1': 'Strongpass99!', 'password2': 'Strongpass99!'
        })
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'already exists')

    def test_authenticated_redirects_away(self):
        User.objects.create_user('u', password='p')
        self.client.login(username='u', password='p')
        r = self.client.get(reverse('register'))
        self.assertRedirects(r, '/')


class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('loginuser', password='Testpass99!')

    def test_login_get(self):
        r = self.client.get(reverse('login'))
        self.assertEqual(r.status_code, 200)

    def test_login_success(self):
        r = self.client.post(reverse('login'), {'username': 'loginuser', 'password': 'Testpass99!'})
        self.assertRedirects(r, '/')

    def test_login_wrong_password(self):
        r = self.client.post(reverse('login'), {'username': 'loginuser', 'password': 'wrongpass'})
        self.assertEqual(r.status_code, 200)

    def test_logout(self):
        self.client.login(username='loginuser', password='Testpass99!')
        r = self.client.get(reverse('logout'))
        self.assertRedirects(r, '/')


class DashboardTest(TestCase):
    def test_dashboard_requires_login(self):
        r = self.client.get(reverse('dashboard'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('/accounts/login/', r['Location'])

    def test_dashboard_authenticated(self):
        User.objects.create_user('dash', password='Testpass99!')
        self.client.login(username='dash', password='Testpass99!')
        r = self.client.get(reverse('dashboard'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Dashboard')
