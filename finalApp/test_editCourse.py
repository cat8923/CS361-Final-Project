from django.test import TestCase
from django.test import Client

from finalApp.models import MyUser, CourseData, CourseSections, LabData



class editCourse(TestCase):
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
        self.course = CourseSections(course=self.data, section=901, instructor=self.temp1)

        self.Lab = LabData(course=self.course, section=902)


def test_01(self):
    response1 = self.client.post("/Login/", {'name': 'user', 'password': 'pass'})
    self.assertEqual("/Homepage/", response1.url, "Valid Information will take to the homepage page")

    response = self.client.post("/Edit_Course/", {"Description": "Introduction to Software Engineering",
                                                    "Designation": "CS361-901", "Semester": "Spring 2021",
                                                    "Instructor": 1, "role": "TA", "Lab": 902})

    self.assertEqual(response.url, "/Homepage/")

    # test if the account that was created above can login. If so then It was successfully created and it works

    response1 = self.client.post("/Login/", {'name': 'bic21', 'password': 'hello'})
    self.assertEqual("/HomePage/", response1.url, "Valid Information will take to the homepage page")


def test_01_Invalid(self):
    response1 = self.client.post("/Login/", {'name': 'user', 'password': 'pass'})
    self.assertEqual("/Homepage/", response1.url, "Valid Information will take to the homepage page")

    response = self.client.post("/Edit_Course/", {"Description": 12121,
                                                    "Designation": "CS361-201", "Semester": "Spring 1995",
                                                    "Instructor": 1, "role": "TA", "Lab": 901})

    self.assertEqual("/Create_Course/", response.url, "Invalid type")

    # test if the account that was created above can login. If so then It was succesfully created and it works

    response1 = self.client.post("/Login/", {'name': 'bic21', 'password': 'hello'})
    self.assertEqual("/Homepage/", response1.url, "Valid Information will take to the homepage page")
