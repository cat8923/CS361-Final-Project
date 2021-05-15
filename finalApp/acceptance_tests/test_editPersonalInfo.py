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
        self.TA_user = MyUser(position="T", username='TA01')
        self.TA_user.set_password(raw_password='pass2')


        self.test_instructor_info = MyUser.objects.create(myName='Test Instructor', phoneNumber='414-555-5501', addressl1= '4306 Griff Street',
                                                           email='csdept@example.com',)

        self.test_TA_info = MyUser.objects.create(myName='Test TA', phoneNumber='414-341-1102', addressl1='706 Offshore Drive',
                                                  email='Tcsdept@example.com', )

    # changing the phone number
    def test_IN(self):
        # login
        response = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response.url, '/Homepage/')

        response = self.client.post(reverse('editself'), {"username": "prof01", "first_name": "Test", "last_name": "Instructor",
                                                          "phone_number": "416-320-5501",
                                                          "email": "csdept@example.com",
                                                          "addressln1": "4306 Griff Street"})

        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 1)


        user = MyUser.objects.get(username__iexact="prof01")
        self.assertEqual(user.phone_number, "416-320-5501")

    # changing email
    def test_IN2(self):
        # login
        response = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response.url, '/Homepage/')

        response1 = self.client.post(reverse('editself'), {"username": "prof01", "first_name": "Test",
                                                           "last_name": "Instructor", "phone_number": "416-555-5501",
                                                           "email": "csdept@uwm.com",
                                                           "addressln1": "4306 Griff Street"})
        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 1)

        user = MyUser.objects.get(username__iexact= "prof01")
        self.assertEqual(user.email, "csdept@uwm.edu")

        # changing address

    def test_IN3(self):
        # login
        response = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response.url, '/Homepage/')

        response2 = self.client.post(reverse('editself'), {"username": "prof01", "first_name": "Test Instructor",
                                                           "last_name": "Instructor", "phone_Number": "416-555-5501",
                                                           "email": "csdept@example.com",
                                                           "addressln1": "4316 Red Street"})
        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 1)

        user = MyUser.objects.get(username__iexact= "prof01")
        self.assertEqual(user.address, "4316 Red Street")


    # changing the phone number
    def test_TA1(self):
        # login
        response2 = self.client.post(reverse('login'), {'username': 'TA01', 'password': 'pass2'})
        self.assertEqual(response2.url, '/Homepage/')

        response3 = self.client.post(reverse('editself'),{"username": "TA01", "first_name": "Test TA",
                                                         "last_name": "TA", "phone_number": "414-855-2201",
                                                        "email": "Tcsdept@example.com",
                                 "                      addressln1": "706 Offshore Drive"})

        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 1)

        user1 = MyUser.objects.get(username__iexact="TA01")
        self.assertEqual(user1.phone_number, "414-855-2201")

    # changing email

    def test_TA2(self):
        # login
        response2 = self.client.post(reverse('login'), {'username': 'TA01', 'password': 'pass2'})
        self.assertEqual(response2.url, '/Homepage/')

        response4 = self.client.post(reverse('editself'), {"username": "TA01", "first_name": "Test TA",
                                                            "last_name": "TA", "phone_number": "414-341-1102",
                                                            "email": "mss@uwm.edu",
                                                            "addressln1": "706 Offshore Drive"})
        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 1)

        user1 = MyUser.objects.get(username__iexact="TA01")
        self.assertEqual(user1.email, "mss@uwm.edu")

    # changing address


    def test_TA3(self):
        # login
        response2 = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response2.url, '/Homepage/')

        response5 = self.client.post(reverse('editself'), {"username": "TA01", "first_name": "Test TA",
                                                       "last_name": "TA", "phone_number": "414-341-1102",
                                                       "email": "Tc@uwm.edu",
                                                       "addressln1": "320 Blue Aster Dr"})
        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 1)

        user1 = MyUser.objects.get(username__iexact="prof01")
        self.assertEqual(user1.addressln1, "320 Blue Aster Dr")