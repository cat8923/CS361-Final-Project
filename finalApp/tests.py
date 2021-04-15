from django.test import TestCase
from .models import MyUser
# Create your tests here.


class DbCreateTest(TestCase):
    def setUp(self):
        pass

    def test_createUser(self):
        temp = MyUser(username="user1", first_name="john", last_name="doe")
        temp.set_password(raw_password="pass1")
        temp.save()
        print()