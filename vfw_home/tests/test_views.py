from django.urls import resolve
from django.http import HttpRequest
from django.test import TestCase
from vfw_home.views import HomeView, LogoutView,LoginView
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.urls import reverse

def setUpUsers():
    """

    @return:
    @rtype:
    """
    test_admin_layer = User.objects.create(username='admin_layer')
    test_admin_layer.set_password('123456')
    test_admin_layer.is_authenticated = True
    test_admin_layer.is_superuser = True
    test_admin_layer.save()

    test_user = User.objects.create(username='boncho')
    test_user.set_password('123456')
    test_user.save()

    test_user2 = User.objects.create(username='evlogi')
    test_user2.set_password('123456')
    test_user2.save()

    return {'test_admin_layer':test_admin_layer,'test_user':test_user,'test_user2':test_user2}

class HomeViewTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'vfw_home/home/')

class LogoutViewTest(TestCase):
    def test_uses_home_template(self):
       response = self.client.get('/')
       self.assertTemplateUsed(response, 'vfw_home/home/')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'logout': 'logged out'})
        print(response.content.decode())
        self.assertIn('{} logged out', response.content.decode()) #todo!

        self.assertRedirects(response, expected_url='vfw_home/home/', status_code=302, target_status_code=200)

class LoginViewTest(TestCase):
    def test_uses_home_template(self):
       response = self.client.get('/')
       self.assertTemplateUsed(response, 'vfw_home/home/')

    def setUp(self):
        self.credentials = {
            'username': 'admin_layer',
            'password': '123456'}
        User.objects.create_user(**self.credentials)

    def test_login_as_admin_layer(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(self.client.login(username='admin_layer', password='123456'))
        response = self.client.get(reverse('account:login'))
        self.assertRedirects(response, expected_url='vfw_home/home/rsp/login/init...', status_code=302, target_status_code=200)
