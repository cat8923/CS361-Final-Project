from django.test import TestCase
from .models import MyUser, UserType
# Create your tests here.


class DbCreateTest(TestCase):
    def setUp(self):
        for i in range(5):
            temp = MyUser(username = "user" + str(i), first_name="john" + str(i), last_name="doe" + str(i))
            temp.set_password(raw_password="pass" + str(i))
            temp.save()

        temp = MyUser(username="user5", first_name="john5", last_name="doe5", position=UserType.SUPERVISOR)
        temp.set_password(raw_password="pass5")
        temp.save()

    def test_createUser(self):
        temp = MyUser.objects.get(username="user1")
        self.assertTrue(temp.has_usable_password())
        self.assertFalse(temp.check_password("pass2"))
        print(list(map(str, MyUser.objects.filter(position = UserType.TA))))
        print(list(map(str, MyUser.objects.filter(position = UserType.SUPERVISOR))))