from django.test import TestCase
from django.test import Client
from Final_Project.models import MyUser

class testCreateLab(TestCase):
    def setUp(self):
        self.Client = Client()
        self.Client.session["position"] = "S"
        self.Client.session.save()

        # creates 3 users (user0, user1, user2)
        # for i in range(3):
        self.temp = MyUser(username="user", first_name="john", last_name="deer", position="S")
        self.temp.set_password(raw_password="pass")
        self.temp.save()

        self.temp1 = MyUser(username="user1", first_name="john", last_name="deer", position="T")
        self.temp1.set_password(raw_password="pass")
        self.temp1.save()


    def test_01(self):
        response1 = self.client.post("/Login/", {'name': 'user', 'password': 'pass'})
        self.assertEqual("/Homepage/", response1.url, "Valid Information will take to the homepage page")

        response = self.client.post("/Create_Lab/", {"Description": "Introduction to Software Engineering",
                                                        "Course": "CS361-901", "Semester": "Spring 2021",
                                                        "Instructor": "Jayson Rock","role": "TA",
                                                     "Times": "Tu & Thur 10:00-10:50 AM"})

        self.assertEqual(response.url, "/Homepage/")


    def test_01_Invalid(self):
        response1 = self.client.post("/Login/", {'name': 'user', 'password': 'pass'})
        self.assertEqual("/Homepage/", response1.url, "Valid Information will take to the homepage page")

        response = self.client.post("/CreateLab/", {"Description": "Introduction",
                                                        "Course": "CS361-909", "Semester": "Spring 2021",
                                                        "Instructor": "Jayson Rock","role": "TA",
                                                     "Times": "Tu & Thur 6:00-6:50 AM"})

        self.assertEqual("/CreateLab/", response.url, "Invalid type")



