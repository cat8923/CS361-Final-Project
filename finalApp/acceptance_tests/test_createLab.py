from django.test import TestCase
from django.test import Client
from django.urls import reverse
from finalApp.models import MyUser


class testCreateLab(TestCase):
    def setUp(self):
        self.client = Client()

        # creates 3 users (user0, user1, user2)
        # for i in range(3):
        self.temp = MyUser(username="user", first_name="john", last_name="deer", position="S")
        self.temp.set_password(raw_password="pass")
        self.temp.save()

        self.temp1 = MyUser(username="user1", first_name="john", last_name="deer", position="T")
        self.temp1.set_password(raw_password="pass")
        self.temp1.save()

    def test_01(self):
        response1 = self.client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        response = self.client.post("/Create_Lab/", {"title": "Introduction to Software Engineering",
                                                     "designation": "CS361", "semester": "Spring 2021"}, follow=True)

        self.assertEqual(response.request["PATH_INFO"], "/Homepage/")

    def test_01_Invalid(self):
        response1 = self.client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        response = self.client.post("/CreateLab/", {"title": "Introduction",
                                                    "designation": "CS361", "semester": "Spring 2021"})

        self.assertEqual("/CreateLab/", response.request["PATH_INFO"], "Invalid type")