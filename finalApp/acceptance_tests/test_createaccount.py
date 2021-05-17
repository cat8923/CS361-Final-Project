from django.test import TestCase
from django.test import Client
from django.urls import reverse
from finalApp.models import MyUser, UserType


class TestCreateAccount(TestCase):
    def setUp(self):
        self.Client = Client()
        self.Client.session["position"] = "S"
        self.Client.session.save()

        # creates 3 users (user0, user1, user2)
        # for i in range(3):
        self.temp = MyUser(username="user", first_name="john", last_name="deer", position="S")
        self.temp.set_password(raw_password="pass")
        self.temp.save()
        
    def test_noAccount(self):
        response = self.Client.post(reverse('createaccount'),
                                    {"username": "bic21", "password": "hello", "first_name": "brett",
                                     "last_name": "frank", "addressln1": "3423 N Maryland",
                                     "addressln2": "Milwaukee, WI",
                                     "title": str(UserType.SUPERVISOR), "email": "test@test.com",
                                     "number": "123456789"})
        self.assertEqual(response.context.get("message"), "successfully created account",
                         msg="did not confirm account creation")
        self.assertEqual(response.request["PATH_INFO"], reverse('createaccount'))
        users = list(MyUser.objects.all())
        self.assertEqual(len(users), 4, msg="Error: the extra user is not created")

    def test_makeManyAccount(self):
        response = self.Client.post(reverse('createaccount'),
                                    {"username": "bic21", "password": "hello", "first_name": "brett",
                                     "last_name": "frank", "addressln1": "3423 N Maryland",
                                     "addressln2": "Milwaukee, WI",
                                     "title": str(UserType.SUPERVISOR), "email": "test@test.com",
                                     "number": "123456789"})

        self.assertEqual(response.context.get("message"), "successfully created account",
                         msg="did not confirm account creation")

        response = self.Client.post(reverse('createaccount'),
                                    {"username": "bic22", "password": "hello", "first_name": "brett",
                                     "last_name": "frank", "addressln1": "3423 N Maryland",
                                     "addressln2": "Milwaukee, WI",
                                     "title": str(UserType.SUPERVISOR), "email": "test@test.com",
                                     "number": "123456789"})

        self.assertEqual(response.context.get("message"), "successfully created account",
                         msg="did not confirm account creation for second account")

        self.assertEqual(response.request["PATH_INFO"], reverse('createaccount'))
        users = list(MyUser.objects.all())
        self.assertEqual(len(users), 5, msg="Error: the extra user is not created")

    def test_accountExists(self):
        response = self.Client.post(reverse('createaccount'),
                                    {"username": "user1", "password": "pass1", "first_name": "brett",
                                     "last_name": "frank", "addressln1": "3423 N Maryland",
                                     "addressln2": "Milwaukee, WI",
                                     "title": str(UserType.SUPERVISOR), "email": "test@test.com",
                                     "number": "123456789"})
        self.assertEqual(response.context.get("message"), "Error: username user1 is already taken",
                         msg="account was not created")
        self.assertEqual(response.request["PATH_INFO"], reverse('createaccount'))
