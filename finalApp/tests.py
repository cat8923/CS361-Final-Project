from django.test import TestCase
from .models import MyUser, UserType, CourseData, LabData, TAsToCourses
from .database_access import make_user, login, ErrorString


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
        check = login({"username": "user0", "password": "pass0"})
        temp = MyUser.objects.get(username="user0")
        self.assertTrue(check, msg="Error: correct login information does not login user")
        self.assertTrue(type(check) is dict, msg="Error: login does not return a dictionary")
        needed = ["first_name", "last_name", "position"]
        self.assertListEqual(list(check.keys()), needed, msg="Error: login returns a dictionary with incorrect keys")
        self.assertEqual(check["first_name"], temp.first_name,
                         msg="Error: login dictionary returns incorrect first name")
        self.assertEqual(check["last_name"], temp.last_name, msg="Error: login dictionary returns incorrect last name")
        self.assertEqual(check["position"], temp.position, msg="Error: login dictionary returns incorrect position")

    def test_wrongPass(self):
        check = login({"username": "user0", "password": "pass1"})
        self.assertFalse(check, msg="Error: logging in with incorrect password returns True")
        self.assertTrue(type(check) is ErrorString, msg="Error: bad password does not return ErrorString")
        self.assertEqual(str(check), "Error: incorrect password",
                         msg="Error: bad password does not return correct error message")

    def test_userDoesNotExist(self):
        check = login({"username": "user0", "password": "pass0"})
        self.assertFalse(check, msg="Error: logging in with incorrect username returns True")
        self.assertTrue(type(check) is ErrorString, msg="Error: bad username does not return ErrorString")
        self.assertEqual(str(check), "Error: user does not exist",
                         msg="Error: bad username does not return correct error message")

    def test_multiLogin(self):
        needed = ["first_name", "last_name", "position"]
        for i in range(3):
            tempusername = "user" + str(i)
            temppass = "pass" + str(i)
            check = login({"username": tempusername, "password": temppass})
            temp = MyUser.objects.get(username=tempusername)
            self.assertTrue(check, msg="Error: correct login information does not login user")
            self.assertTrue(type(check) is dict, msg="Error: login does not return a dictionary")
            self.assertListEqual(list(check.keys()), needed,
                                 msg="Error: login returns a dictionary with incorrect keys")
            self.assertEqual(check["first_name"], temp.first_name,
                             msg="Error: login dictionary returns incorrect first name")
            self.assertEqual(check["last_name"], temp.last_name,
                             msg="Error: login dictionary returns incorrect last name")
            self.assertEqual(check["position"], temp.position, msg="Error: login dictionary returns incorrect position")

    def test_missingData(self):
        check = login({"username": "user0"})
        self.assertFalse(check, msg="Error: logging in without password returns True")
        self.assertTrue(type(check) is ErrorString, msg="Error: missing password does not return ErrorString")
        self.assertEqual(str(check), "Error: password not provided",
                         msg="Error: missing password does not return correct error message")

        check = login({"password": "pass0"})
        self.assertFalse(check, msg="Error: logging in without username returns True")
        self.assertTrue(type(check) is ErrorString, msg="Error: missing username does not return ErrorString")
        self.assertEqual(str(check), "Error: username not provided",
                         msg="Error: missing username does not return correct error message")


class CreateCourseTest(TestCase):
    def setUp(self):
        pass

    def test_goodData(self):
        pass

    def test_badData(self):
        pass

    def test_courseExists(self):
        pass

    def test_instructorDoesNotExist(self):
        pass

    def test_missingData(self):
        pass


class CreateLabTest(TestCase):
    def setUp(self):
        pass

    def test_goodData(self):
        pass

    def test_badData(self):
        pass

    def test_labExists(self):
        pass

    def test_courseDoesNotExist(self):
        pass

    def test_taDoesNotExist(self):
        pass

    def test_missingData(self):
        pass


class AssignTALabTest(TestCase):
    def setUp(self):
        pass

    def test_goodData(self):
        pass

    def test_badData(self):
        pass

    def test_taDoesNotExist(self):
        pass

    def test_labDoesNotExist(self):
        pass

    def test_missingData(self):
        pass


class AssignInstructorCourseTest(TestCase):
    def setUp(self):
        pass

    def test_goodData(self):
        pass

    def test_badData(self):
        pass

    def test_courseDoesNotExist(self):
        pass

    def test_instructorDoesNotExist(self):
        pass

    def test_missingData(self):
        pass
