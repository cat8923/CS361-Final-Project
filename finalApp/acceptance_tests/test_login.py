from django.test import TestCase
from django.test import Client
from django.urls import reverse
from finalApp.models import MyUser, UserType


class testLogin(TestCase):
    def setUp(self):
            self.Client = Client()

            self.temp = MyUser(username="Supervisor", first_name="Susan", last_name="Mcroy", position=UserType.SUPERVISOR)
            self.temp.set_password(raw_password="pass")
            self.temp.save()

            self.temp1 = MyUser(username="Instructor", first_name="Jason", last_name="Rock", position=UserType.INSTRUCTOR)
            self.temp1.set_password(raw_password="pass1")
            self.temp1.save()

            self.temp2 = MyUser(username="TA", first_name="Apoorv", last_name="Prasad", position=UserType.TA)
            self.temp2.set_password(raw_password="pass2")
            self.temp2.save()

    def test_valid_login_S(self):
        response = self.client.post(reverse('login'), {'username': 'Supervisor','password': 'pass'}, follow=True)
        self.assertEqual("/Homepage/", response.request["PATH_INFO"], "Valid Information will take to the homepage page")
        # after a successful login it should take the user to the homescreen

    def test_invalid_login_S(self):
        response = self.client.post(reverse('login'), {'username': 'Supervisor', 'password': '123'})
        self.assertEqual("Error: bad username or password", response.context['message'], "InValid Information will take back to home page")

    def test_valid_login_I(self):
        response = self.client.post(reverse('login'), {'username': 'Instructor','password': 'pass1'}, follow=True)
        self.assertEqual("/Homepage/", response.request["PATH_INFO"], "Valid Information will take to the homepage page")

    def test_invalid_login_I(self):
        response = self.client.post(reverse('login'), {'username': 'Instructor', 'password': '123'}, follow=True)
        self.assertEqual("Error: bad username or password", response.context['message'], "InValid Information does not take back to home page")

    def test_valid_login_TA(self):
        response = self.client.post(reverse('login'), {'username': 'TA','password': 'pass2'}, follow=True)
        self.assertEqual("/Homepage/", response.request["PATH_INFO"], "Valid Information will take to the homepage page")

    def test_invalid_login_TA(self):
        response = self.client.post(reverse('login'), {'username': 'TA', 'password': '123'})
        self.assertEqual("Error: bad username or password", response.context['message'], "InValid Information does not take back to home page")