from django.test import TestCase
from django.test import Client
from finalApp.models import MyUser, UserType

class testDeleteAccount(TestCase):
    def setup(self):
        self.client = Client()
        self.Client.session["position"] = "S"
        self.Client.session.save()

        # creates 3 users (user0, user1, user2)
        for i in range(3):
            temp = MyUser(username="user" + str(i), first_name="john" + str(i), last_name="deer" + str(i))
            temp.set_password(raw_password="pass" + str(i))
            temp.save()

