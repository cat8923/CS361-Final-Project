from django.test import TestCase
from django.test import Client
from finalApp.models import MyUser

class testLogin(TestCase):
    def setUp(self):
            self.Client = Client()
            self.Client.session["position"] = "S"
            self.Client.session.save()

            self.temp = MyUser(username="Supervisor", first_name="Susan", last_name="Mcroy", position="S")
            self.temp.set_password(raw_password="pass")
            self.temp.save()

            self.temp1 = MyUser(username="Instructor", first_name="Jason", last_name="Rock", position="I")
            self.temp1.set_password(raw_password="pass1")
            self.temp1.save()

            self.temp2 = MyUser(username="TA", first_name="Apoorv", last_name="Prasad", osition="TA")
            self.temp2.set_password(raw_password="pass2")
            self.temp2.save()

    def test_valid_login_S(self):
        response = self.client.post("/", {'name': 'Supervisor','password': 'pass'})
        self.assertEqual("/Homepage/",response.url, "Valid Information will take to the homepage page")
        # after a successful login it should take the user to the homescreen
        print(response.context['MyUser'])


    def test_invalid_login_S(self):
        response = self.client.post("/", {'name': 'Supervisor', 'password': '123'})
        self.assertEqual("Error: Incorrect Password", response.context['message'], "InValid Information will take back to home page")

    def test_valid_login_I(self):
        response = self.client.post("/", {'name': 'Instructor','password': 'pass1'})
        self.assertEqual("/Homepage/",response.url, "Valid Information will take to the homepage page")

    def test_invalid_login_I(self):
        response = self.client.post("/", {'name': 'Instructor', 'password': '123'})
        self.assertEqual("Error: Incorrect Password", response.context['message'], "InValid Information will take back to home page")

    def test_valid_login_TA(self):
        response = self.client.post("/", {'name': 'TA','password': 'pass2'})
        self.assertEqual("/Homepage/",response.url, "Valid Information will take to the homepage page")

    def test_invalid_login_TA(self):
        response = self.client.post("/", {'name': 'TA', 'password': '123'})
        self.assertEqual("Error: Incorrect Password", response.context['message'], "InValid Information will take back to home page")
