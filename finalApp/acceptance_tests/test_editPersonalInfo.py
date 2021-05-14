from django.test import TestCase
from django.test import Client
from django.urls import reverse
from finalApp.models import MyUser


class TestAddPersonalInfo(TestCase):
    def setUp(self):
        self.client = Client()
        self.instructor_user = MyUser(position="I", username='prof01')
        self.instructor_user.set_password(raw_password='pass')
        self.instructor_user.save()
        self.Client = Client()
        # self.Client.session["position"] = "S"
        # self.Client.session.save()

        # self.test_instructor_info = PersonalInfo.objects.create(myName='Test Instructor', phoneNumber='414-555-5501', addressl1= '4306 Griff Street',
        #                                                   email='csdept@example.com',)

    # changing the phone number
    def test_01(self):
        # login
        response = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response.url, '/Homepage/')

        response = self.client.post(reverse('editself'), {"username": "prof01", "first_name": "Test", "last_name": "Instructor",
                                                          "phone_number": "416-555-5501",
                                                          "email": "csdept@example.com",
                                                          "addressln1": "4306 Griff Street"})

        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 1)

        # for i in self.pi:
        #     if i.phoneNumber == "416-555-5501":
        #         self.assertTrue("Successfully edited phone number")
        user = MyUser.objects.get(username__iexact="prof01")
        self.assertEqual(user.phone_number, "416-555-5501")

    # changing email
    def test_02(self):
        # login
        response = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response.url, '/Homepage/')

        response1 = self.client.post(reverse('editself'), {"username": "prof01", "first_name": "Test",
                                                           "last_name": "Instructor", "phone_number": "416-555-5501",
                                                           "email": "csdept@uwm.com",
                                                           "addressln1": "4306 Griff Street"})

        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 1)

        for i in self.pi:
            if i.email == "csdept@uwm.edu":
                self.assertTrue("Successfully added personal info")

        # changing address

    def test_03(self):
        # login
        response = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response.url, '/Homepage/')

        response2 = self.client.post(reverse('editself'), {"username": "prof01", "name": "Test Instructor",
                                                           "PhoneNumber": "416-555-5501",
                                                           "email": "csdept@uwm.com",
                                                           "addressln1": "4316 Red Street"})
        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 1)

        for i in self.pi:
            if i.email == "csdept@uwm.edu":
                self.assertTrue("Successfully added personal info")
