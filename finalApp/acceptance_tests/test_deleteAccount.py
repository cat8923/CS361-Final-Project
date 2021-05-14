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

    def test_1(self):

            response = self.client.post("/", {'username': 'Supervisor', 'password': 'pass'}, follow=True)
            self.assertEqual("/Homepage/", response.request["PATH_INFO"],"Valid Information will take to the homepage page")

            # add a user
            response1 = self.Client.post("/create_account/", {"username": "bic21", "password": "hello", "first_name": "brett",
                                                         "last_name": "frank", "address": "3423 N Maryland",
                                                         "title": str(UserType.SUPERVISOR), "email": "test@test.com",
                                                         "number": "123456789"})
            self.assertEqual(response1.context.get("message"), "successfully created account",msg="did not confirm account creation")


            response2 = self.client.post('/edit_account/', {"User": 2})


            response3 = self.client.get('/account_list/')

            users = list(response3.context['users'])
            print(users)


            if len(users) == 1:
                self.assertTrue("Successful Deletion")
            else:
                self.assertFalse("Successful Deletion")

        def test_2(self):
            pass