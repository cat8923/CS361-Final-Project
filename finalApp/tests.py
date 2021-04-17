from django.test import TestCase
from .models import MyUser, UserType, CourseData, LabData, TAsToCourses
from .database_access import make_user, login


# Create your tests here.


class DbCreateTest(TestCase):
    def setUp(self):
        pass
        # for i in range(5):
        #    temp = MyUser(username = "user" + str(i), first_name="john" + str(i), last_name="doe" + str(i))
        #    temp.set_password(raw_password="pass" + str(i))
        #    temp.save()

        # temp = MyUser(username="user5", first_name="john5", last_name="doe5", position=UserType.SUPERVISOR)
        # temp.set_password(raw_password="pass5")
        # temp.save()

    def test_createUser(self):
        make_user({"username": "user1", "password": "pass1", "first_name": "john", "last_name": "doe",
                   "address": "3400 N Maryland", "title": UserType.SUPERVISOR, "email": "test@test.com",
                   "number": "123456789"})

        check = make_user({"username": "user1", "password": "pass1", "first_name": "john", "last_name": "doe",
                           "address": "3400 N Maryland", "title": UserType.SUPERVISOR, "email": "test@test.com",
                           "number": "123456789"})

        if check:
            print(check)
        else:
            temp = MyUser.objects.get(username="user1")
            self.assertTrue(temp.has_usable_password())
            self.assertFalse(temp.check_password("pass2"))
            print(list(map(str, MyUser.objects.filter(position=UserType.TA))))
            print(list(map(str, MyUser.objects.filter(position=UserType.SUPERVISOR))))


class UserLoginTest(TestCase):
    def setUp(self):
        for i in range(3):
            temp = MyUser(username="user" + str(i), first_name="john" + str(i), last_name="doe" + str(i))
            temp.set_password(raw_password="pass" + str(i))
            temp.save()

    def test_goodLogin(self):
        check = login({"username":"user0", "password":"pass0"})
        temp = MyUser.objects.get(username="user0")
        self.assertTrue(check, msg="Error: correct login information does not login user")
        self.assertTrue(type(check) is dict, msg="Error: login does not return a dictionary")
        needed = ["first_name", "last_name", "position"]
        self.assertListEqual(list(check.keys()), needed, msg="Error: login returns a dictionary with incorrect keys")
        self.assertEqual(check["first_name"], temp.first_name, msg="Error: login dictionary returns incorrect first name")
        self.assertEqual(check["last_name"], temp.last_name, msg="Error: login dictionary returns incorrect last name")
        self.assertEqual(check["position"], temp.position, msg="Error: login dictionary returns incorrect position")
