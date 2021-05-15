from django.test import TestCase
from django.test import Client
from django.urls import reverse
from finalApp.models import MyUser, TASkills


class TestAddPersonalInfo(TestCase):
    def setUp(self):
        self.client = Client()
        self.instructor_user = MyUser(position="I", username='prof01')
        self.instructor_user.set_password(raw_password='pass')
        self.instructor_user.save()

        self.ta_user = MyUser(position="T", username="ta01")
        self.ta_user.set_password(raw_password='pass')
        self.ta_user.save()

    # changing the phone number
    def test_updatePhoneNumber(self):
        # login
        response = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response.url, reverse('home'), msg="Error: logging in does not redirect properly")

        response = self.client.post(reverse('editself'), {"username": "prof01", "first_name": "Test", "last_name": "Instructor",
                                                          "phone_number": "416-555-5501",
                                                          "email": "csdept@example.com",
                                                          "addressln1": "4306 Griff Street"})

        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 2, msg="Error: an extra user is created when trying to update user data")

        # for i in self.pi:
        #     if i.phoneNumber == "416-555-5501":
        #         self.assertTrue("Successfully edited phone number")
        user = MyUser.objects.get(username__iexact="prof01")
        self.assertEqual(user.phone_number, "416-555-5501")

    # changing email
    def test_updateEmail(self):
        # login
        response = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response.url, reverse('home'), msg="Error: logging in does not redirect properly")

        response1 = self.client.post(reverse('editself'), {"username": "prof01", "first_name": "Test",
                                                           "last_name": "Instructor", "phone_number": "416-555-5501",
                                                           "email": "csdept@uwm.com",
                                                           "addressln1": "4306 Griff Street"})

        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 2, msg="Error: an extra user is created when trying to update user data")

        self.assertEqual(MyUser.objects.get(username="prof01").email, "csdept@uwm.com", msg="Error: email is not updated")

    # changing address
    def test_updateAddress(self):
        # login
        response = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response.url, reverse('home'), msg="Error: logging in does not redirect properly")

        response2 = self.client.post(reverse('editself'), {"username": "prof01", "name": "Test Instructor",
                                                           "phone_number": "416-555-5501",
                                                           "email": "csdept@uwm.edu",
                                                           "addressln1": "4316 Red Street",
                                                           "addressln2": "Milwaukee, WI"})
        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 2, msg="Error: an extra user is created when trying to update user data")

        self.assertEqual(MyUser.objects.get(username="prof01").addressln1, "4316 Red Street", msg="Error: address is not updated")
        self.assertEqual(MyUser.objects.get(username="prof01").addressln2, "Milwaukee, WI", msg="Error: address is not updated")

    def test_updateTASkills(self):
        response = self.client.post(reverse('login'), {'username': 'ta01', 'password': 'pass'})
        self.assertEqual(response.url, reverse('home'), msg="Error: logging in does not redirect properly")

        response1 = self.client.post(reverse('editself'), {"username": "ta01", "first_name": "ta",
                                                           "last_name": "ta", "phone_number": "416-555-5501",
                                                           "email": "csdept@uwm.com",
                                                           "skills": "Grading"})

        self.pi = MyUser.objects.all()
        self.assertEqual(len(self.pi), 2, msg="Error: an extra user is created when trying to update user data")
        self.assertEqual(TASkills.objects.get(TA__username="ta01").skills, "Grading", msg="Error: skills are not updated")
