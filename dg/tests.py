from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class LoginTest(TestCase):
    """This class checks login page"""
    fixtures = ['test_database.json']

    def test_login_page_opens(self):
        """This method checks profile page"""
        client = Client()
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_page_redirect(self):
        """This function returns dictionary value by key"""
        client = Client()
        user = User.objects.get(username='g')
        client.force_login(user=user)

        response = client.get(reverse("login"), follow=True)
        self.assertEqual(response.status_code, 200)


class IndexTest(TestCase):
    """This class checks index page"""
    fixtures = ['test_database.json']  # manage.py dumpdata to get it

    def setUp(self):
        # self.client = Client(enforce_csrf_checks=True)
        # сверху штука Для проверки csrf-токенов
        self.client = Client()
        self.user = User.objects.get(username='g')
        self.client.login(username='test_user', password='promprog')  # для проверки авторизации
        self.client.force_login(user=self.user)  # для быстрой авторизации

    def test_index_page_opens(self):
        """This method checks index page"""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_redirect(self):
        """This method checks login page redirect"""
        unauth_client = Client()
        response = unauth_client.get(reverse("index"), follow=True)
        self.assertRedirects(response, reverse('login'))
        url = response.redirect_chain[-1]
        self.assertIn(reverse("login"), url)

    def test_send_message_unlogged(self):
        """This method checks unlogged guy messages"""
        unauth_client = Client()
        response = unauth_client.post(reverse("send_message"),
                                      data={'text': 'Super idol', 'chat_id': 1})
        self.assertEqual(response.status_code, 302)


class LogoutTest(TestCase):
    """This class checks logout staff"""
    fixtures = ['test_database.json']

    def test_logoutn_page_opens(self):
        """This method checks logout page"""
        client = Client()
        user = User.objects.get(username='g')
        client.force_login(user=user)
        response = client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class RegisterTest(TestCase):
    """This class checks register page"""
    fixtures = ['test_database.json']

    def test_create_user(self):
        """This method checks user creation"""
        client = Client()
        data = {
            'username': 'teset_user2',
            'password': 'pass',
            'password2': 'pass',
        }
        response = client.post(reverse('register'), data=data, follow=True)
        self.assertRedirects(response, reverse('login'))

    def test_get_register_page(self):
        """This method checks register page"""
        client = Client()
        response = client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)


class ProfileTest(TestCase):
    """This class checks profile page"""
    fixtures = ['test_database.json']

    def test_profile_page_opens(self):
        """This method checks profile page"""
        client = Client()
        user = User.objects.get(username='g')
        client.force_login(user=user)
        response = client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_page_redirects(self):
        """This method checks profile page redirect"""
        client = Client()
        response = client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_page_post(self):
        """This method checks profile page posting"""
        client = Client()
        user = User.objects.get(username='g')
        client.force_login(user=user)
        response = client.post(reverse('profile'), {'old_password': 'g', 'new_password': 'g'})
        self.assertEqual(response.status_code, 302)


class GlobalChatTest(TestCase):
    """This class checks global chat page"""
    fixtures = ['test_database.json']

    def test_page_open(self):
        """This method checks test page"""
        client = Client()
        response = client.get(reverse('global_chat'))
        self.assertEqual(response.status_code, 200)
