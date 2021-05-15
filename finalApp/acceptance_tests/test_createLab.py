from django.test import TestCase
from django.test import Client
from django.urls import reverse
from finalApp.models import MyUser, LabData, CourseData


class TestCreateLab(TestCase):
    def setUp(self):
        self.Client = Client()
        # self.Client.session["position"] = "S"
        # self.Client.session.save()

        # creates 3 users (user0, user1, user2)
        # for i in range(3):
        self.temp = MyUser(username="user", first_name="john", last_name="deer", position="S")
        self.temp.set_password(raw_password="pass")
        self.temp.save()

        self.temp1 = MyUser(username="user1", first_name="john", last_name="deer", position="T")
        self.temp1.set_password(raw_password="pass")
        self.temp1.save()

        CourseData.objects.create(designation="CS361")

    def test_createLab(self):
        response1 = self.client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        response = self.client.post(reverse('addsection', args=['CS361']), {"section": "901", "isLab": "on"},
                                    follow=True)

        self.assertEqual(response.request["PATH_INFO"], reverse('addsection', args=['CS361']),
                         msg="Error: creating a lab section redirects to the wrong page")

        labs = list(LabData.objects.all())
        self.assertEqual(len(labs), 1, msg="Error: wrong number of labs created")
        self.assertEqual(labs[0].section, 901, msg="Error: lab is created with wrong section")
        self.assertEqual(labs[0].course, CourseData.objects.get(designation="CS361"),
                         msg="Error: lab is not assigned to the right course")

    def test_createManyLab(self):
        response1 = self.client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        self.client.post(reverse('addsection', args=['CS361']), {"section": "901", "isLab": "on"},
                                    follow=True)

        response = self.client.post(reverse('addsection', args=['CS361']), {"section": "902", "isLab": "on"},
                                    follow=True)

        self.assertEqual(response.request["PATH_INFO"], reverse('addsection', args=['CS361']),
                         msg="Error: creating a lab section redirects to the wrong page")

        labs = list(LabData.objects.all())
        self.assertEqual(len(labs), 2, msg="Error: wrong number of labs created")
        self.assertEqual(labs[1].section, 902, msg="Error: lab is created with wrong section")
        self.assertEqual(labs[1].course, CourseData.objects.get(designation="CS361"),
                         msg="Error: lab is not assigned to the right course")

    def test_createDuplicateLab(self):
        response1 = self.client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        self.client.post(reverse('addsection', args=['CS361']), {"section": "901", "isLab": "on"},
                                    follow=True)

        response = self.client.post(reverse('addsection', args=['CS361']), {"section": "901", "isLab": "on"},
                                    follow=True)

        self.assertEqual(response.request["PATH_INFO"], reverse('addsection', args=['CS361']),
                         msg="Error: creating a lab section redirects to the wrong page")

        labs = list(LabData.objects.all())
        self.assertEqual(len(labs), 1, msg="Error: an extra lab is creatd")
        self.assertEqual(labs[0].section, 901, msg="Error: adding duplicate lab changes section")
        self.assertEqual(labs[0].course, CourseData.objects.get(designation="CS361"),
                         msg="Error: adding duplicate lab changes course of first")

    def test_makeLabInvalid(self):
        response1 = self.client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response1.request["PATH_INFO"],
                         "Valid Information will take to the homepage page")

        response = self.client.post("/CreateLab/", {"title": "Introduction",
                                                    "designation": "CS361", "semester": "Spring 2021"})

        self.assertEqual("/CreateLab/", response.request["PATH_INFO"], "Invalid type")
