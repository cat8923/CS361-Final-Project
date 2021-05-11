from django.test import TestCase
from django.test import Client
from finalApp.models import MyUser, TASkills


class testAddSkills(TestCase):
    def setUp(self):
        self.Client = Client()

        # creates 3 users (user0, user1, user2)
        for i in range(3):
            temp = MyUser(username="user" + str(i), first_name="john" + str(i), last_name="deer" + str(i))
            temp.set_password(raw_password="pass" + str(i))
            temp.save()

    def test01(self):
        response1 = self.client.post("/Login/", {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual("/Homepage/", response1.request["PATH_INFO"], "Valid Information will take to the homepage page")




