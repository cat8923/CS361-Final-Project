from django.test import TestCase
from django.test import Client
from Final_Project.models import MyUser, UserType,CourseData, CourseSections


class edit_Account(TestCase):
    def setUp(self):
        self.Client = Client()
        self.Client.session["position"] = "S"
        self.Client.session.save()

        # creates 3 users (user0, user1, user2)
        # for i in range(3):
        self.temp = MyUser(username="user", first_name="john", last_name="deer", position="S")
        self.temp.set_password(raw_password="pass")
        self.temp.save()

        self.temp1 = MyUser(username="user1", first_name="john", last_name="deer", position="I")
        self.temp1.set_password(raw_password="pass")
        self.temp1.save()

        self.data = CourseData(title="Cs")

        self.course = CourseSections(course=self.data, section=901)


    def test_noAccount(self):
        response1 = self.client.post("/Login/", {'name': 'user', 'password': 'pass'})
        self.assertEqual("/HomePage/", response1.url, "Valid Information will take to the homepage page")

        response = self.Client.post("/edit_account/",
                                    {"username": "user1", "password": "bye", "first_name": "Bob",
                                     "last_name": "frank", "address": "3423 N Maryland",
                                     "title": "I", "email": "test@test.com",
                                     "number": "123456789"})

        self.assertEqual(response.context["message"], "successfully edited account", msg="confirmed account edit")
        self.assertEqual(response.url, "/HomePage/")



    def test_accountExists(self):
        response = self.Client.post("/edit_account/",
                                    {"username": "user2", "password": "pass5", "first_name": "Bryan",
                                     "last_name": "Johnson", "address": "3429 N Maryland",
                                     "title": UserType.SUPERVISOR, "email": "test@test.com",
                                     "number": "123456789"})
        self.assertEqual(response.context["message"], "account already exists", msg="account was not created")
        self.assertEqual(response.url, "/create_account/")
