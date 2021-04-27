from django.test import TestCase
from django.test import Client
from Final_Project.models import MyUser,CourseData, LabData, TAsToCourses


class assignTA(TestCase):
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
        self.course = TAsToCourses(course=self.data, section=901, instructor= self.temp1)

        self.Lab = LabData(course=self.course, section=902)

    def test_01(self):
        response1 = self.client.post("/Login/", {'name': 'user', 'password': 'pass'})
        self.assertEqual("/Homepage/", response1.url, "Valid Information will take to the homepage page")

        response = self.Client.post("/create_account/",
                                    {"username": "bic21", "password": "hello", "first_name": "brett",
                                     "last_name": "frank", "address": "3423 N Maryland",
                                     "title": "TA", "email": "test@test.com",
                                     "number": "123456789"})
        self.assertEqual(response.context["message"], "successfully created account", msg="confirmed account creation")
        self.assertEqual(response.url, "/HomePage/")

        # assign the user created to the course declared in setUp
        response2 = self.Client.post("/Create_Lab/", {"Lab": 1})
        self.assertEqual(response2.url, "/Homepage/")



    def test_02(self):
        response1 = self.client.post("/Login/", {'name': 'user', 'password': 'pass'})
        self.assertEqual("/HomePage/", response1.url, "Valid Information will take to the homepage page")

        response = self.Client.post("/create_account/",
                                    {"username": "bic21", "password": "hello", "first_name": "brett",
                                     "last_name": "frank", "address": "3423 N Maryland",
                                     "title": "TA", "email": "test@test.com",
                                     "number": "123456789"})

        self.assertEqual(response.context["message"], "successfully created account", msg="confirmed account creation")
        self.assertEqual(response.url, "/Homepage/")


        # assign the user created to the course declared in setUp
        response2 = self.Client.post("/Create_Lab/", {"Lab": 2})
        self.assertEqual("/Create_Lab/", response2.url,"Lab does not exist")