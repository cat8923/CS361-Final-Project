from django.test import TestCase
from django.test import Client

from finalApp.models import MyUser


class testCreateCourses(TestCase):
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


    def test_01(self):
        response1 = self.client.post("/Login/", {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual("/Homepage/", response1.request["PATH_INFO"], "Valid Information will take to the homepage page")

        response = self.client.post("/Create_Course/", {"Description": "CS 361-Introduction to Software Engineering",
                                                        "Section": "201", "Semester": "Spring 2021",
                                                        "Instructor": 1,"role": "TA", "Lab": 901})

        self.assertEqual(response.url, "/Homepage/")

        # test if the account that was created above can login. If so then It was successfully created and it works

        response1 = self.client.post("/Login/", {'username': 'bic21', 'password': 'hello'})
        self.assertEqual("/Homepage/", response1.request["PATH_INFO"], "Valid Information will take to the homepage page")

    def test_01_Invalid(self):
        response1 = self.client.post("/Login/", {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual("/Homepage/", response1.request["PATH_INFO"], "Valid Information will take to the homepage page")

        response = self.client.post("/Create_Course/", {"Description": 12121,
                                                        "Section": "201", "Semester": "Spring 2021",
                                                        "Instructor": 1, "role": "TA", "Lab": 901})

        self.assertEqual("/Create_Course/", response.url, "Invalid type")

        # test if the account that was created above can login. If so then It was succesfully created and it works

        response1 = self.client.post("/Login/", {'name': 'bic21', 'password': 'hello'}, follow=True)
        self.assertEqual("/Homepage/", response1.request["PATH_INFO"], "Valid Information will take to the homepage page")
