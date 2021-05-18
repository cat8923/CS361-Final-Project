from django.test import TestCase
from django.test import Client
from django.urls import reverse
from finalApp.models import MyUser, CourseData, CourseSections, UserType, TASkills


class TestEditAccount(TestCase):
    def setUp(self):
        self.Client = Client()
        self.Client.session["position"] = "S"
        self.Client.session.save()

        # creates 3 users (user0, user1, user2)
        # for i in range(3):
        self.temp = MyUser(username="user", first_name="john", last_name="deer", position="S")
        self.temp.set_password(raw_password="pass")
        self.temp.save()

        self.temp1 = MyUser(username="user1", first_name="jim", last_name="dean", position="I")
        self.temp1.set_password(raw_password="pass")
        self.temp1.save()

        self.temp2 = MyUser(username="user2", first_name="jack", last_name="daniels", position="T")
        self.temp2.set_password(raw_password="pass")
        self.temp2.save()

        self.data = CourseData(title="Cs")

        self.course = CourseSections(course=self.data, section=901)

        self.TA = TASkills(skills="Math")

    def test_noAccount(self):
        response1 = self.Client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        response = self.Client.post(reverse('editaccount'),
                                    {"username": "user1", "password": "bye", "first_name": "Bob",
                                     "last_name": "frank", "address": "3423 N Maryland",
                                     "title": "I", "email": "test@test.com",
                                     "number": "123456789", "onclick": "Save Edits"}, follow=True)

        self.assertEqual("Success!", response.context.get("message"), msg="confirmed account edit")
        self.assertEqual(response.request["PATH_INFO"], reverse('editaccount'), msg="Error: redirects to wrong page")

    def test_AsTA(self):
        response2 = self.Client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response2.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        response3 = self.Client.post(reverse('editaccount'),
                                     {"username": "user2", "password": "pass5", "first_name": "Jack",
                                      "last_name": "Daniels", "address": "3429 N Maryland",
                                      "title": UserType.TA, "email": "test@test.com",
                                      "number": "123456789", "Skills": "Math", "onclick": "Save Edits"}, follow=True)

        self.assertEqual("Success!", response3.context.get("message"),
                         msg="skills have not been added")

    def test_ASSP(self):
        response1 = self.Client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        response = self.Client.post(reverse('editaccount'),
                                    {"username": "user1", "first_name": "Bryan",
                                     "last_name": "Johnson", "address": "3429 N Maryland",
                                     "title": "TA", "email": "test@test.com",
                                     "number": "123456789", "onclick": "Save Edits"}, follow=True)
        self.assertEqual("Success!", response.context.get("message"), msg="account was not edited")

    def test_accountExists(self):
        response1 = self.Client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        response = self.Client.post(reverse('editaccount'),
                                    {"username": "user2", "password": "pass5", "first_name": "Bryan",
                                     "last_name": "Johnson", "address": "3429 N Maryland",
                                     "title": UserType.SUPERVISOR, "email": "test@test.com",
                                     "number": "123456789", "onclick": "Save Edits"}, follow=True)
        self.assertEqual("Success!", response.context.get("message"), msg="account was not created")

        self.assertEqual(reverse('editaccount'), response.request["PATH_INFO"], msg="Error: redirects to wrong page")
