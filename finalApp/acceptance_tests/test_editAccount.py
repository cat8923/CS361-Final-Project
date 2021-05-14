from django.test import TestCase
from django.test import Client

from finalApp.models import MyUser, CourseData, CourseSections, UserType, TASkills



class testEditAccount(TestCase):
    def setUp(self):
        self.Client = Client()
        self.Client.session["position"] = "S"
        self.Client.session.save()

        # creates 3 users (user0, user1, user2)
        # for i in range(3):
        self.temp = MyUser(username="user", first_name="john", last_name="deer", position="S")
        self.temp.set_password(raw_password="pass")
        self.temp.save()

        self.temp1 = MyUser(username="user1", first_name="jim", last_name="dean", position="I")
        self.temp1.set_password(raw_password="pass")
        self.temp1.save()

        self.temp2 = MyUser(username="user2", first_name="jack", last_name="daniels", position="T")
        self.temp1.set_password(raw_password="pass")
        self.temp1.save()



        self.data = CourseData(title="Cs")

        self.course = CourseSections(course=self.data, section=901)

        self.TA = TASkills(skills= "Math")



    def test_01(self):
        response1 = self.client.post("/", {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual("/Homepage/", response1.request["PATH_INFO"], "Valid Information will take to the homepage page")

    def test_noAccount(self):
        response1 = self.client.post("/Login/", {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual("/HomePage/", response1.request["PATH_INFO"], "Valid Information will take to the homepage page")


        response = self.Client.post("/edit_account/",
                                    {"username": "user1", "password": "bye", "first_name": "Bob",
                                     "last_name": "frank", "address": "3423 N Maryland",
                                     "title": "I", "email": "test@test.com",
                                     "number": "123456789"})

        self.assertEqual(response.context["message"], "successfully edited account", msg="confirmed account edit")
        self.assertEqual(response.url, "/HomePage/")

     def test_AsTA(self):
         response2 = self.client.post("/Login/", {'username': 'user2', 'password': 'pass'}, follow=True)
         self.assertEqual("/HomePage/", response2.request["PATH_INFO"], "Valid Information will take to the homepage page")

         response3 = self.Client.post("/edit_account/",
                                {"username": "user2", "password": "pass5", "first_name": "Jack",
                                 "last_name": "Daniels", "address": "3429 N Maryland",
                                 "title": UserType.TA, "email": "test@test.com",
                                 "number": "123456789", "Skills": "Math"})

         self.assertEqual(response3.context.get("message"), "skills for TA updated successfully", msg="skills have not been added")


    def test_ASSP(self):
        response1 = self.client.post("/", {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual("/Homepage/", response1.request["PATH_INFO"], "Valid Information will take to the homepage page")

        response = self.Client.post("/edit_account/",
                                    {"username": "user1", "password": 1234, "first_name": "Bryan",
                                     "last_name": "Johnson", "address": "3429 N Maryland",
                                     "title": "TA", "email": "test@test.com",
                                     "number": "123456789",})
        self.assertEqual(response.context.get("message"), "invalid credentials", msg="account was not edited")

    def test_accountExists(self):
        response = self.Client.post("/edit_account/",
                                    {"username": "user2", "password": "pass5", "first_name": "Bryan",
                                     "last_name": "Johnson", "address": "3429 N Maryland",
                                     "title": UserType.SUPERVISOR, "email": "test@test.com",
                                     "number": "123456789"})
        self.assertEqual(response.context.get("message"), "account already exists", msg="account was not created")

        self.assertEqual(response.url, "/create_account/")
