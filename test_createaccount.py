from django.test import TestCase
from django.test import Client
from .models import MyUser, UserType


class createAccount(TestCase):
    def setUp(self):
        self.Client = Client()
        self.Client.session["position"] = "S"
        self.Client.session.save()

        # creates 3 users (user0, user1, user2)
        for i in range(3):
            temp = MyUser(username="user" + str(i), first_name="john" + str(i), last_name="deer" + str(i))
            temp.set_password(raw_password="pass" + str(i))
            temp.save()


    def test_noAccount(self):
        response = self.Client.post("/create_account/", {"username": "bic21", "password": "hello", "first_name": "brett",
                                                         "last_name": "frank", "address": "3423 N Maryland",
                                                         "title": UserType.SUPERVISOR, "email": "test@test.com",
                                                         "number": "123456789"})
        self.assertEqual(response.context["message"], "successfully created account", msg="confirmed account creation")
        self.assertEqual(response.url, "/edit_account/")


    def test_accountExists(self):
        response = self.Client.post("/create_account/", {"username": "user1", "password": "pass1", "first_name": "brett",
                                                         "last_name": "frank", "address": "3423 N Maryland",
                                                         "title": UserType.SUPERVISOR, "email": "test@test.com",
                                                         "number": "123456789"})
        self.assertEqual(response.context["message"], "account already exists", msg="account was not created")
        self.assertEqual(response.url, "/create_account/")
        