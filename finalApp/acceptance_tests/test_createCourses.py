from django.test import TestCase
from django.test import Client
from django.urls import reverse
from finalApp.models import MyUser, CourseData, CourseSections


class TestCreateCourses(TestCase):
    def setUp(self):
        self.Client = Client()
        # self.Client.session["position"] = "S"
        # self.Client.session.save()

        # creates 3 users (user0, user1, user2)
        # for i in range(3):
        self.temp = MyUser(username="user", first_name="john", last_name="deer", position="S")
        self.temp.set_password(raw_password="pass")
        self.temp.save()

        self.temp1 = MyUser(username="user1", first_name="john", last_name="deer", position="I")
        self.temp1.set_password(raw_password="pass")
        self.temp1.save()

    def test_createCourse(self):
        response1 = self.client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        response = self.client.post("/Create_Course/", {"title": "Introduction to Software Engineering",
                                                        "designation": "CS361",
                                                        "section": 201, "semester": "SP21"})

        self.assertEqual(response.request["PATH_INFO"], "/Create_Course/")

        courses = list(CourseData.objects.all())
        sections = list(CourseSections.objects.all())

        self.assertEqual(len(courses), 1, msg="Error: the wrong number of courses is created")
        self.assertEqual(len(sections), 1, msg="Error: the wrong number of sections is created")

        self.assertEqual(courses[0].title, "Introduction to Software Engineering",
                         msg="Error: created course has wrong title")
        self.assertEqual(courses[0].designation, "CS361", msg="Error: created course has wrong designation")
        self.assertEqual(sections[0].section, 201, msg="Error: created section has wrong section number")

    def test_createCourseDuplicate(self):
        response1 = self.client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        self.client.post("/Create_Course/", {"title": "Introduction to Software Engineering",
                                             "designation": "CS361",
                                             "section": 201, "semester": "SP21"})

        response = self.client.post("/Create_Course/", {"title": "Introduction to Software Engineering",
                                                        "designation": "CS361",
                                                        "section": 201, "semester": "SP21"})

        self.assertEqual(response.request["PATH_INFO"], "/Create_Course/")

        courses = list(CourseData.objects.all())
        sections = list(CourseSections.objects.all())

        self.assertEqual(len(courses), 1, msg="Error: an extra course is created")
        self.assertEqual(len(sections), 1, msg="Error: an extra section is created")

        self.assertEqual(courses[0].title, "Introduction to Software Engineering",
                         msg="Error: created course has wrong title")
        self.assertEqual(courses[0].designation, "CS361", msg="Error: created course has wrong designation")
        self.assertEqual(sections[0].section, 201, msg="Error: created section has wrong section number")

    def test_createCourseMany(self):
        response1 = self.client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        self.client.post("/Create_Course/", {"title": "Introduction to Software Engineering",
                                             "designation": "CS361",
                                             "section": 201, "semester": "SP21"})

        response = self.client.post("/Create_Course/", {"title": "Introduction to CS",
                                                        "designation": "CS250",
                                                        "section": 201, "semester": "SP21"})

        self.assertEqual(response.request["PATH_INFO"], "/Create_Course/")

        courses = list(CourseData.objects.all())
        sections = list(CourseSections.objects.all())

        self.assertEqual(len(courses), 2, msg="Error: the wrong number of courses is created")
        self.assertEqual(len(sections), 2, msg="Error: the wrong number of sections is created")

        self.assertEqual(courses[1].title, "Introduction to CS", msg="Error: created course has wrong title")
        self.assertEqual(courses[1].designation, "CS250", msg="Error: created course has wrong designation")
        self.assertEqual(sections[1].section, 201, msg="Error: created section has wrong section number")

    def test_createCourseBadData(self):
        response1 = self.client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        response = self.client.post("/Create_Course/", {"title": 12121,
                                                        "section": "201", "semester": "Spring 2021",
                                                        "Instructor": 1, "role": "TA", "Lab": 901})

        self.assertEqual("/Create_Course/", response.request["PATH_INFO"], "Invalid type")

        courses = list(CourseData.objects.all())
        sections = list(CourseSections.objects.all())

        self.assertEqual(len(courses), 0, msg="Error: the wrong number of courses is created")
        self.assertEqual(len(sections), 0, msg="Error: the wrong number of sections is created")
