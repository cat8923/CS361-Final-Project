from django.test import TestCase
from django.test import Client
from finalApp.models import MyUser, UserType


class testCreateAccount(TestCase):
    def setUp(self):
        self.Client = Client()
        self.Client.session["position"] = "S"
        self.Client.session.save()

        # creates 3 users (user0, user1, user2)
        # for i in range(3):
        self.temp = MyUser(username="user", first_name="john", last_name="deer", position="S")
        self.temp.set_password(raw_password="pass")
        self.temp.save()

        self.data = CourseData(title="Cs")

        self.course = CourseSections(course=self.data, section=901)

    def test_noAccount(self):
        response1 = self.client.post("/Login/", {'name': 'user', 'password': 'pass'})
        self.assertEqual("/Homepage/", response1.url, "Valid Information will take to the homepage page")

        response = self.Client.post("/create_account/",
                                    {"username": "bic21", "password": "hello", "first_name": "brett",
                                     "last_name": "frank", "address": "3423 N Maryland",
                                     "title": "I", "email": "test@test.com",
                                     "number": "123456789"})

        self.assertEqual(response.context["message"], "successfully created account", msg="confirmed account creation")
        self.assertEqual(response.url, "/HomePage/")

        # assign the user created to the course declared in setUp
        response2 = self.Client.post("/account/", {"users": 1})
        self.assertEqual(response2.url, "/Assign_Course/")

        response3 = self.Client.post("/Assign_Course/", {"courses": 1})
        self.assertEqual(response3.url, "/HomePage/")

    def test_accountExists(self):
        response = self.Client.post("/create_account/",
                                    {"username": "user1", "password": "pass1", "first_name": "brett",
                                     "last_name": "frank", "address": "3423 N Maryland",
                                     "title": UserType.SUPERVISOR, "email": "test@test.com",
                                     "number": "123456789"})
        self.assertEqual(response.context["message"], "account already exists", msg="account was not created")
        self.assertEqual(response.url, "/create_account/")
