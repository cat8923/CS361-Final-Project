from django.test import TestCase
from django.test import Client
from django.urls import reverse
from finalApp.models import MyUser, UserType


class CreateAccount(TestCase):
    def setUp(self):
        self.Client = Client()

        # creates 3 users (user0, user1, user2)
        sup = MyUser(username="super", position="S")
        sup.set_password(raw_password="pass")
        sup.save()

        for i in range(3):
            temp = MyUser(username="user" + str(i), first_name="john" + str(i), last_name="deer" + str(i))
            temp.set_password(raw_password="pass" + str(i))
            temp.save()

    def test_noAccount(self):
        self.Client.post(reverse('login'), {"username": "super", "password": "pass"})

        response = self.Client.post("/create_account/",
                                    {"username": "bic21", "password": "hello", "first_name": "brett",
                                     "last_name": "frank", "addressln1": "3423 N Maryland",
                                     "addressln2": "Milwaukee, WI",
                                     "title": "S", "email": "test@test.com",
                                     "number": "123456789"})
        self.assertEqual(response.context.get("message"), "successfully created account",
                         msg="did not confirm account creation")
        self.assertEqual(response.request["PATH_INFO"], "/create_account/")

    def test_accountExists(self):
        self.Client.post(reverse('login'), {"username": "super", "password": "pass"})

        response = self.Client.post("/create_account/",
                                    {"username": "user1", "password": "pass1", "first_name": "brett",
                                     "last_name": "frank", "addressln1": "3423 N Maryland", "addressln2": "Milwaukee, WI",
                                     "title": str(UserType.SUPERVISOR), "email": "test@test.com",
                                     "number": "123456789"})
        self.assertEqual(response.context.get("message"), "Error: username user1 is already taken",
                         msg="account was not created")
        self.assertEqual(response.request["PATH_INFO"], "/create_account/")
