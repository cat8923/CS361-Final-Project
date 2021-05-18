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

        self.TA_user = MyUser(position="T", username='TA01')
        self.TA_user.set_password(raw_password='pass2')
        self.instructor_user.save()


        self.test_instructor_info = MyUser.objects.create(myName='Test Instructor', phoneNumber='414-555-5501', addressl1= '4306 Griff Street',
                                                           email='csdept@example.com',)

        self.test_TA_info = MyUser.objects.create(myName='Test TA', phoneNumber='414-341-1102', addressl1='706 Offshore Drive',
                                                  email='Tcsdept@example.com', )

    # changing the phone number
    def test_updatePhoneNumberIN(self):
        # login
        response = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response.url, reverse('home'), msg="Error: logging in does not redirect properly")

        response = self.client.post(reverse('editself'), {"username": "prof01", "first_name": "Test", "last_name": "Instructor",
                                                          "phone_number": "416-320-5501",
                                                          "email": "csdept@example.com",
                                                          "addressln1": "4306 Griff Street"})

        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 2, msg="Error: an extra user is created when trying to update user data")


        user = MyUser.objects.get(username__iexact="prof01")
        self.assertEqual(user.phone_number, "416-320-5501")

    # changing email
    def test_updatedEmailIN(self):
        # login
        response = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response.url, '/Homepage/')

        response1 = self.client.post(reverse('editself'), {"username": "prof01", "first_name": "Test",
                                                           "last_name": "Instructor", "phone_number": "416-555-5501",
                                                           "email": "csdept@uwm.com",
                                                           "addressln1": "4306 Griff Street"})
        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 2, msg="Error: an extra user is created when trying to update user data")

        self.assertEqual(MyUser.objects.get(username="prof01").email, "csdept@uwm.com",
                         msg="Error: email is not updated")

        # changing address

    def test_updateAddressIN(self):
        # login
        response = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response.url, '/Homepage/')

        response2 = self.client.post(reverse('editself'), {"username": "prof01", "first_name": "Test Instructor",
                                                           "last_name": "Instructor", "phone_Number": "416-555-5501",
                                                           "email": "csdept@example.com",
                                                           "addressln1": "4316 Red Street"})
        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 2, msg="Error: an extra user is created when trying to update user data")

        self.assertEqual(MyUser.objects.get(username="prof01").addressln1, "4316 Red Street",
                         msg="Error: address is not updated")
        self.assertEqual(MyUser.objects.get(username="prof01").addressln2, "Milwaukee, WI",
                         msg="Error: address is not updated")


    # changing the phone number
    def test_updatePhoneNumberTA(self):
        # login
        response2 = self.client.post(reverse('login'), {'username': 'TA01', 'password': 'pass2'})
        self.assertEqual(response2.url, '/Homepage/')

        response3 = self.client.post(reverse('editself'),{"username": "TA01", "first_name": "Test TA",
                                                         "last_name": "TA", "phone_number": "414-855-2201",
                                                        "email": "Tcsdept@example.com",
                                                        "addressln1": "706 Offshore Drive"})

        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 2, msg="Error: an extra user is created when trying to update user data")

        user1 = MyUser.objects.get(username__iexact="TA01")
        self.assertEqual(user1.phone_number, "414-855-2201")

    # changing email

    def test_updatedEmailTA(self):
        # login
        response2 = self.client.post(reverse('login'), {'username': 'TA01', 'password': 'pass2'})
        self.assertEqual(response2.url, '/Homepage/')

        response4 = self.client.post(reverse('editself'), {"username": "TA01", "first_name": "Test TA",
                                                            "last_name": "TA", "phone_number": "414-341-1102",
                                                            "email": "mss@uwm.edu",
                                                            "addressln1": "706 Offshore Drive"})
        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 2, msg="Error: an extra user is created when trying to update user data")

        user1 = MyUser.objects.get(username__iexact="TA01")
        self.assertEqual(user1.email, "mss@uwm.edu")

    # changing address


    def test_updateAddressTA (self):
        # login
        response2 = self.client.post(reverse('login'), {'username': 'prof01', 'password': 'pass'})
        self.assertEqual(response2.url, '/Homepage/')

        response5 = self.client.post(reverse('editself'), {"username": "TA01", "first_name": "Test TA",
                                                       "last_name": "TA", "phone_number": "414-341-1102",
                                                       "email": "Tc@uwm.edu",
                                                       "addressln1": "320 Blue Aster Dr"})
        self.pi = MyUser.objects.all()

        self.assertEqual(len(self.pi), 2, msg="Error: an extra user is created when trying to update user data")

        user1 = MyUser.objects.get(username__iexact="prof01")
        self.assertEqual(user1.addressln1, "320 Blue Aster Dr")

    def test_updateTASkills(self):
        response = self.client.post(reverse('login'), {'username': 'ta01', 'password': 'pass'})
        self.assertEqual(response.url, reverse('home'), msg="Error: logging in does not redirect properly")
        response1 = self.client.post(reverse('editself'), {"username": "ta01", "first_name": "ta",
                                                               "last_name": "ta", "phone_number": "416-555-5501",
                                                               "email": "csdept@uwm.com",
                                                               "skills": "Grading"})
        self.pi = MyUser.objects.all()
        self.assertEqual(len(self.pi), 2, msg="Error: an extra user is created when trying to update user data")
        self.assertEqual(TASkills.objects.get(TA__username="ta01").skills, "Grading",
                             msg="Error: skills are not updated")