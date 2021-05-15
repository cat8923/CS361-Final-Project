from django.test import TestCase
from django.test import Client
from django.urls import reverse
from finalApp.models import MyUser,CourseData, LabData, TAsToCourses, UserType, CourseSections


class testAssignI(TestCase):
    def setUp(self):
        self.Client = Client()


        self.temp1 = MyUser(username="user1", first_name="john", last_name="deer", position=UserType.INSTRUCTOR)
        self.temp1.set_password(raw_password="pass")
        self.temp1.save()

        self.ta = MyUser(username="I", position=UserType.I)
        self.ta.save()

        self.data = CourseData(title="Class", designation="CS1")
        self.data.save()
        self.course = CourseSections(course=self.data, section=901, instructor= self.temp1)
        self.course.save()

    def test_01(self):
        response = self.client.post(reverse('login'), {'username': 'Instructor', 'password': 'pass1'}, follow=True)
        self.assertEqual("/Homepage/", response.request["PATH_INFO"], "Valid Information will take to the homepage page")

        response = self.Client.post("/create_account/",
                                    {"username": "bic21", "password": "hello", "first_name": "brett",
                                     "last_name": "frank", "addressln1": "3423 N Maryland", "addressln2": "Milwaukee wi",
                                     "title": "TA", "email": "test@test.com",
                                     "number": "123456789"})

        self.assertEqual(response.context.get("message"), "successfully created account", msg="No message for confirmed account creation")
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"])

        # assign the user created to the course declared in setUp
        response2 = self.Client.post("/Create_Course/", {"Course": 1}, follow=True)
        self.assertEqual(reverse('home'), response2.request['PATH_INFO'])

    def test_02(self):
        response1 = self.client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)

        self.assertEqual(reverse('home'), response1.request["PATH_INFO"], "Valid Information will take to the homepage page")

        response = self.Client.post("/create_account/",
                                    {"username": "bic21", "password": "hello", "first_name": "brett",
                                     "last_name": "frank", "addressln1": "3423 N Maryland","addressln2": "Milwaukee WI",
                                     "title": "TA", "email": "test@test.com",
                                     "number": "123456789"})

        self.assertEqual(response.context["message"], "successfully created account", msg="confirmed account creation")
        self.assertEqual(reverse('home'), response.request["PATH_INFO"])

        # assign the user created to the course declared in setUp
        response2 = self.Client.post("/Create_Course/", {"Course": 2})
        self.assertEqual("/Create_Course/", response2.request["PATH_INFO"],"Lab does not exist")