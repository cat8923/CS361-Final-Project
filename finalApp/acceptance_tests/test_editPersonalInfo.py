from django.test import TestCase
from django.test import Client
from finalApp.models import Users, PersonalInfo



class TestAddPersonalInfo(TestCase):
    def setUp(self):
        self.client = Client()
        self.instructor_user = Users.objects.create(role="Instructor", user_username='prof01',
                                                    user_password='pass')
        self.Client = Client()
        self.Client.session["position"] = "S"
        self.Client.session.save()


        for i in range(3):
            temp = MyUser(username="user" + str(i), first_name="john" + str(i), last_name="deer" + str(i))
            temp.set_password(raw_password="pass" + str(i))
            temp.save()

        self.test_instructor_info = PersonalInfo.objects.create(myName='Test Instructor', phoneNumber='414-555-5501',
                                                           email='csdept@example.com',)


    # changing the phone number
    def test_01(self):
        # login
        response = self.client.post('/', {'loginEmail': 'prof01', 'loginPassword': 'pass'})
        self.assertEqual(response.url, '/userView')

        response = self.client.post('/AddPersonalInfo/', {"name": "Test Instructor", "PhoneNumber": "416-555-5501", "email": "csdept@example.com", })

        self.pi = PersonalInfo.objects.all()

        self.assertEqual(len(self.pi), 1)

        for i in self.pi:
                if i.phoneNumber == "416-555-5501":
                    self.assertTrue("Successfully edited phone number")

    # changing email
    def test_02(self):
        # login
        response = self.client.post('/', {'loginEmail': 'prof01', 'loginPassword': 'pass'})
        self.assertEqual(response.url, '/userView')

        response = self.client.post('/AddPersonalInfo/', {"name": "Test Instructor", "PhoneNumber": "416-555-5501", "email": "csdept@uwm.com",})

        self.pi = PersonalInfo.objects.all()

        self.assertEqual(len(self.pi), 1)

        for i in self.pi:
                if i.myName == "csdept@uwm.edu":
                    self.assertTrue("Successfully added personal info")

