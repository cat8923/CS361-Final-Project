from django.test import TestCase
from django.test import Client
from django.urls import reverse
from finalApp.models import MyUser, CourseData, LabData, TAsToCourses, UserType, CourseSections


class TestAssignTA(TestCase):
    def setUp(self):
        self.Client = Client()
        # self.Client.session["position"] = "S"
        # self.Client.session.save()

        # creates 3 users (user0, user1, user2)
        # for i in range(3):
        self.temp = MyUser(username="user", first_name="john", last_name="deer", position=UserType.SUPERVISOR)
        self.temp.set_password(raw_password="pass")
        self.temp.save()

        self.temp1 = MyUser(username="user1", first_name="john", last_name="deer", position=UserType.INSTRUCTOR)
        self.temp1.set_password(raw_password="pass")
        self.temp1.save()

        self.ta = MyUser(username="TA", position=UserType.TA)
        self.ta.save()

        self.data = CourseData(title="Class", designation="CS1")
        self.data.save()
        self.course = CourseSections(course=self.data, section=901, instructor=self.temp1)
        self.course.save()

        self.Lab = LabData(course=self.data, section=902)
        self.Lab.save()

    def test_assignTaToCourse(self):
        response = self.Client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response.request['PATH_INFO'],
                         "Valid Information does not take to the homepage page")

        url = reverse('assigntas', args=['CS1'])
        response = self.Client.post(url, {"taUsername": "TA"})
        response = self.Client.post(url, {"taUsername": "TA"})
        self.assertEqual("Error: TA has already been assigned to course", response.context.get("message"),
                         msg="No message for failing assignment")
        self.assertEqual(reverse('assigntas', args=['CS1']), response.request['PATH_INFO'])

        self.assertEqual(1, len(TAsToCourses.objects.all()), msg="Error: wrong number of linking entries created")

    def test_alreadyAssigned(self):
        response = self.Client.post(reverse('login'), {'username': 'user', 'password': 'pass'}, follow=True)
        self.assertEqual(reverse('home'), response.request['PATH_INFO'],
                         "Valid Information does not take to the homepage page")

        url = reverse('assigntas', args=['CS1'])
        response = self.Client.post(url, {"taUsername": "TA"})
        self.assertEqual("Success!", response.context.get("message"), msg="No message for successful assignment")
        self.assertEqual(reverse('assigntas', args=['CS1']), response.request['PATH_INFO'])
        self.assertEqual(1, len(TAsToCourses.objects.all()), msg="Error: wrong number of linking entries created")
