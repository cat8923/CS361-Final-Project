from django.test import TestCase
from finalApp.models import MyUser, UserType, CourseData, LabData, TAsToCourses, CourseSections
from finalApp.database_access import make_user, login, ErrorString, make_course, make_lab, assign_ta_to_lab, assign_instructor, \
    get_course_id_by_name, assign_ta_to_course
import random


# Create your tests here.


class UserCreateTest(TestCase):
    def setUp(self):
        for i in range(4):
            temp = MyUser(username="user" + str(i), first_name="john" + str(i), last_name="doe" + str(i))
            temp.set_password(raw_password="pass" + str(i))
            temp.save()

    def test_createUser(self):
        check = make_user({"username": "user5", "password": "pass5", "first_name": "john", "last_name": "doe",
                           "address": "3400 N Maryland", "title": UserType.SUPERVISOR, "email": "testtest.com",
                           "number": "123456789"})

        self.assertTrue(check, msg="Error: good data does not create user")
        temp = MyUser.objects.get(username="user5")
        self.assertTrue(temp.has_usable_password(), msg="Error: password was not assigned to user")
        self.assertTrue(temp.check_password("pass5"), msg="Error: password does not check out for created acount")

    def test_usernameTaken(self):
        data = {"username": "user1", "password": "pass1", "first_name": "john", "last_name": "doe",
                "address": "3400 N Maryland", "title": UserType.SUPERVISOR, "email": "test@test.com",
                "number": "123456789"}
        make_user(data)
        data["password"] = "pass2"
        check = make_user(data)
        self.assertFalse(check, msg="Error: make user returns true when username is already taken")
        temp = MyUser.objects.get(username="user1")
        self.assertTrue(temp.check_password("pass1"),
                        msg="Error: making another user with same username changes password of orignal user")

    def test_invalidData(self):
        data = {"username": True, "password": "pass1", "first_name": "john", "last_name": "doe",
                "address": "3400 N Maryland", "title": UserType.SUPERVISOR, "email": "test@test.com",
                "number": "123456789"}
        self.assertFalse(make_user(data), msg="Error: bad input data does not fail")
        data["username"] = "user1"
        data["password"] = False
        self.assertFalse(make_user(data), msg="Error: bad password input does not fail")
        data["password"] = "pass1"
        data["title"] = "Supervisor"
        self.assertFalse(make_user(data), msg="Error: bad position input does not fail")


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

    def test_userDoesNotExist(self):
        check = login({"username": "user3", "password": "pass0"})
        self.assertFalse(check, msg="Error: logging in with incorrect username returns True")
        self.assertTrue(type(check) is ErrorString, msg="Error: bad username does not return ErrorString")

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
        check = login({"password": "pass0"})
        self.assertFalse(check, msg="Error: logging in without username returns True")
        self.assertTrue(type(check) is ErrorString, msg="Error: missing username does not return ErrorString")


class CreateCourseTest(TestCase):
    def setUp(self):
        make_course({"title": "course1", "section": 201})

    def test_goodData(self):
        check = make_course({"title": "course0", "section": 200})
        self.assertTrue(check, msg="Error: good course data fails to create course")
        print(list(map(str, CourseSections.objects.all())))

    def test_badData(self):
        check = make_course({"title": "course0", "section": "200"})
        self.assertFalse(check, msg="Error: making course does not fail when input is incorrect")
        self.assertFalse(CourseData.objects.filter(title="course0").exists(),
                         msg="Error: course data is stored when creation failed")

    def test_courseSectionExists(self):
        check = make_course({"title": "course1", "section": 201})
        self.assertFalse(check, msg="Error: making course does not fail when course section exists")
        tempCourse = CourseData.objects.get(title="course1")
        self.assertEqual(len(CourseSections.objects.filter(course=tempCourse, section=201)), 1,
                         msg="Error: extra section is created when data is incorrect")

    def test_existingCourse(self):
        check = make_course({"title": "course1", "section": 202})
        self.assertTrue(check, msg="Error: creating new section for a course fails when it should not")

    def test_missingData(self):
        check = make_course({"title": "course0"})
        self.assertFalse(check, msg="Error: making course does not fail if a section is not provided")

        check = make_course({"section": 201})
        self.assertFalse(check, msg="Error: making course does not fail when title is not provided")

    def test_makeSureItsWorking(self):
        course = CourseData(title="course2")
        course.save()
        section = CourseSections(section=201, course=course)
        section.save()
        section = CourseSections(section=202, course=course)
        section.save()
        course = CourseData(title="course3")
        course.save()
        section = CourseSections(section=201, course=course)
        section.save()
        section = CourseSections(section=202, course=course)
        section.save()
        temp = list(CourseSections.objects.filter(course__title="course1"))
        print(len(temp))
        temp = list(map(str, CourseSections.objects.filter(course__title="course2")))
        print(temp)


class CreateLabTest(TestCase):
    def setUp(self):
        self.tempCourse = CourseData(title="course1", id=1)
        self.tempCourse.save()

    def test_goodData(self):
        check = make_lab({"courseId": 1, "section": 801})
        self.assertTrue(check, msg="Error: creating a lab for a course that exists fails")
        query = list(LabData.objects.filter(course__title="course1"))
        self.assertEqual(len(query), 1, msg="Error: a single lab is not created for a course")
        self.assertEqual(query[0].section, 801, msg="Error: correct section is not created for the lab")

    def test_badData(self):
        check = make_lab({"courseId": "one", "section": 801})
        self.assertFalse(check, msg="Error: bad course id does not fail")
        query = list(LabData.objects.filter(course__title="course1"))
        self.assertEqual(len(query), 0, msg="Error: a lab is created when courseId is bad")

        check = make_lab({"courseId": 1, "section": "801"})
        self.assertFalse(check, msg="Error: bad section id does not fail")
        query = list(LabData.objects.filter(course__title="course1"))
        self.assertEqual(len(query), 0, msg="Error: a lab is created when section id is bad")

    def test_labExists(self):
        make_lab({"courseId": 1, "section": 801})
        check = make_lab({"courseId": 1, "section": 801})
        self.assertFalse(check, msg="Error: making a lab that already exists does not fail")
        query = list(LabData.objects.filter(course__title="course1"))
        self.assertEqual(len(query), 1, msg="Error: there is not exactly 1 lab section when identical data is passed")

    def test_courseDoesNotExist(self):
        check = make_lab({"courseId": 2, "section": 801})
        self.assertFalse(check, msg="Error: making lab does not fail when course does not exist")
        query = list(LabData.objects.all())
        self.assertEqual(len(query), 0, msg="Error: a lab is created when coures does not exist")

    def test_missingData(self):
        check = make_lab({"section": 801})
        self.assertFalse(check, msg="Error: making lab does not fail when courseId is not given")
        query = list(LabData.objects.all())
        self.assertEqual(len(query), 0, msg="Error: a lab is created when coures is not provided")

        check = make_lab({"courseId": 1})
        self.assertFalse(check, msg="Error: making lab does not fail when section is not given")
        query = list(LabData.objects.all())
        self.assertEqual(len(query), 0, msg="Error: a lab is created when section is not given")

    def test_twoLabsOneCourse(self):
        make_lab({"courseId": 1, "section": 801})
        check = make_lab({"courseId": 1, "section": 802})
        self.assertTrue(check, msg="Error: making lab fails when labs for the same course have different sections")
        query = list(LabData.objects.all())
        self.assertEqual(len(query), 2, msg="Error: lab is not created when section is unique.")


class AssignTALabTest(TestCase):
    def setUp(self):
        tempCourse = CourseData.objects.create(title="course1", id=1)
        self.lab = LabData.objects.create(course=tempCourse, section=801)
        self.ta = MyUser.objects.create(username="user1", position=UserType.TA)
        self.notTa = MyUser.objects.create(username="user2", position=UserType.SUPERVISOR)

    def test_goodData(self):
        check = assign_ta_to_lab({"courseId": 1, "labSection": 801, "taUsername": "user1"})
        self.assertTrue(check, msg="Error: good data does not return true for adding TA to lab")
        self.assertTrue(type(check) is bool, msg="Error: something other than a bool is returned on success")
        self.assertEqual(self.lab.TA, self.ta, msg="Error: wrong TA is assigned to lab")
        query = TAsToCourses.objects.all()
        self.assertEqual(len(query), 1, msg="Error: an object is not created in the linking table")
        self.assertEqual(query[0].TA, self.TA, msg="Error: wrong TA is created in linking table")
        self.assertEqual(query[0].lab.title, "course1", msg="Error: wrong course is in the linking table")

    def test_badData(self):
        check = assign_ta_to_lab({"courseId": "1", "labSection": 801, "taUsername": "user1"})
        self.assertFalse(check, msg="Error: bad data for assigning TA to lab does not fail")
        self.assertEqual(None, self.lab.TA, msg="Error: some TA is assigned to lab when bad data is passed")
        self.assertEqual(0, len(TAsToCourses.objects.all()), msg="Error: an entry is created in linking table")

        check = assign_ta_to_lab({"courseId": 1, "labSection": "801", "taUsername": "user1"})
        self.assertFalse(check, msg="Error: bad data for assigning TA to lab does not fail")
        self.assertEqual(None, self.lab.TA, msg="Error: some TA is assigned to lab when bad data is passed")
        self.assertEqual(0, len(TAsToCourses.objects.all()), msg="Error: an entry is created in linking table")

        check = assign_ta_to_lab({"courseId": 1, "labSection": 801, "taUsername": 1})
        self.assertFalse(check, msg="Error: bad data for assigning TA to lab does not fail")
        self.assertEqual(None, self.lab.TA, msg="Error: some TA is assigned to lab when bad data is passed")
        self.assertEqual(0, len(TAsToCourses.objects.all()), msg="Error: an entry is created in linking table")

    def test_taDoesNotExist(self):
        check = assign_ta_to_lab({"courseId": 1, "labSection": 801, "taUsername": "user3"})
        self.assertFalse(check, msg="Error: when TA does not exist assigning TA does not return false")
        self.assertEqual(None, self.lab.TA, msg="Error: TA is assigned to lab when it should not be")

    def test_userNotTA(self):
        check = assign_ta_to_lab({"courseId": 1, "labSection": 801, "taUsername": "user2"})
        self.assertFalse(check, msg="Error: trying to assign a supervisor as a TA does not fail")
        self.assertEqual(None, self.lab.TA, msg="Error: someone is assigned to lab when it should not be")

    def test_labDoesNotExist(self):
        check = assign_ta_to_lab({"courseId": 1, "labSection": 802, "taUsername": "user1"})
        self.assertFalse(check, msg="Error: assigning TA does not fail when it should")
        self.assertEqual(None, self.lab.TA, msg="Error: TA is assigned to lab when it should not be")

    def test_missingData(self):
        check = assign_ta_to_lab({"labSection": 801, "taUsername": "user1"})
        self.assertFalse(check, msg="Error: missing data for assigning TA to lab does not fail")
        self.assertEqual(None, self.lab.TA, msg="Error: some TA is assigned to lab when bad data is passed")
        self.assertEqual(0, len(TAsToCourses.objects.all()), msg="Error: an entry is created in linking table")

        check = assign_ta_to_lab({"courseId": "1", "taUsername": "user1"})
        self.assertFalse(check, msg="Error: bad data for assigning TA to lab does not fail")
        self.assertEqual(None, self.lab.TA, msg="Error: some TA is assigned to lab when bad data is passed")
        self.assertEqual(0, len(TAsToCourses.objects.all()), msg="Error: an entry is created in linking table")

        check = assign_ta_to_lab({"courseId": 1, "labSection": 801})
        self.assertFalse(check, msg="Error: bad data for assigning TA to lab does not fail")
        self.assertEqual(None, self.lab.TA, msg="Error: some TA is assigned to lab when bad data is passed")
        self.assertEqual(0, len(TAsToCourses.objects.all()), msg="Error: an entry is created in linking table")


class AssignTAToCourseTest(TestCase):
    def setUp(self):
        CourseData.objects.create(title="course1", id=1)
        self.ta = MyUser.objects.create(username="user1", position=UserType.TA)
        self.notTa = MyUser.objects.create(username="user2", position=UserType.SUPERVISOR)

    def test_goodData(self):
        check = assign_ta_to_course({"courseId": 1, "taUsername": "user1"})
        self.assertTrue(check, msg="Error: good data does not assign ta to course")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(1, len(query), msg="Error: not 1 object is created in the linking database")
        self.assertEqual(query[0].TA, self.ta, msg="Error: wrong TA is in the linking database")
        self.assertEqual(query[0].course.title, "course1", msg="Error: wrong course is in the linking database")

    def test_badData(self):
        check = assign_ta_to_course({"courseId": "1", "taUsername": "user1"})
        self.assertFalse(check, msg="Error: bad data does not return false")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(0, len(query), msg="Error: an object was created in the linking database")

        check = assign_ta_to_course({"courseId": 1, "taUsername": 1})
        self.assertFalse(check, msg="Error: bad data does not return false")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(0, len(query), msg="Error: an object was created in the linking database")

    def test_userNotTA(self):
        check = assign_ta_to_course({"courseId": 1, "taUsername": "user2"})
        self.assertFalse(check, msg="Error: when given a non-TA's username, assigning a TA does not fail")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(0, len(query), msg="Error: an object was created in the linking database")

    def test_userNotExist(self):
        check = assign_ta_to_course({"courseId": 1, "taUsername": "user3"})
        self.assertFalse(check, msg="Error: nonexistent user does not return false")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(0, len(query), msg="Error: an object was created in the linking database")

    def test_courseNotExist(self):
        check = assign_ta_to_course({"courseId": 2, "taUsername": "user1"})
        self.assertFalse(check, msg="Error: does not return false when course does not exist")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(0, len(query), msg="Error: an object was created in the linking database")

    def test_alreadyAssigned(self):
        assign_ta_to_course({"courseId": 1, "taUsername": "user1"})
        check = assign_ta_to_course({"courseId": "1", "taUsername": "user1"})
        self.assertFalse(check, msg="Error: assigning already assigned TA does not return false")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(1, len(query), msg="Error: an extra object was created in the linking database")


class AssignInstructorCourseTest(TestCase):
    def setUp(self):
        tempCourse = CourseData(title="course1", id=1)
        tempCourse.save()
        CourseSections.objects.create(course=tempCourse, section=201)

    def test_goodData(self):
        check = assign_instructor({"courseId": 1, "courseSection": 201, "instructorUsername": "user1"})
        self.assertTrue(check, msg="Error: good data does not return true")

    def test_badData(self):
        pass

    def test_userNotInstructor(self):
        pass

    def test_courseDoesNotExist(self):
        pass

    def test_instructorDoesNotExist(self):
        pass

    def test_missingData(self):
        pass


class GetCourseIDTest(TestCase):
    def setUp(self):
        for i in range(5):
            CourseData.objects.create(title="course" + str(i), id=i * 2)

    def test_courseExists(self):
        check = get_course_id_by_name("course3")
        self.assertTrue(check, msg="Error: correct course data does not return true")
        self.assertEqual(check, 6, msg="Error: incorrect ID is returned")

    def test_courseDoesNotExist(self):
        check = get_course_id_by_name("course5")
        self.assertFalse(check, msg="Error: course title does not return false")

    def test_differentCapitalization(self):
        check = get_course_id_by_name("Course1")
        self.assertTrue(check, msg="Error: getting course by title is not case insensitive as it should be")
        self.assertEqual(check, 2, msg="Error: variant capitalization returns incorrect course id")

    def test_invalidData(self):
        check = get_course_id_by_name({"course": "course1"})
        self.assertFalse(check, msg="Error: incorrect passed data does not return false")


class UpdateUserDataTest(TestCase):
    pass


class ListCoursesTest(TestCase):
    pass


class ListUsersTest(TestCase):
    pass
