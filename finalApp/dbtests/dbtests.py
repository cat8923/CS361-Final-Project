from django.test import TestCase
from finalApp.models import MyUser, UserType, CourseData, LabData, TAsToCourses, CourseSections
from finalApp.database_access import make_user, login, ErrorString, make_course, make_lab, assign_ta_to_lab, \
    assign_instructor, \
    get_course_id_by_name, assign_ta_to_course, update_user, list_courses, list_users, get_userdata, list_instructors, \
    list_tas, get_coursedata, get_tas_of_course, get_courses_of_instructor, get_all_user_info, get_skills, \
    update_ta_skill, delete_account


# Create your tests here.


class UserCreateTest(TestCase):
    def setUp(self):
        for i in range(4):
            temp = MyUser(username="user" + str(i), first_name="john" + str(i), last_name="doe" + str(i))
            temp.set_password(raw_password="pass" + str(i))
            temp.save()

    def test_createUser(self):
        check = make_user({"username": "user5", "password": "pass5", "first_name": "john", "last_name": "doe",
                           "addressln1": "3400 N Maryland", "addressln2": "Milwaukee, WI 53211",
                           "title": str(UserType.SUPERVISOR), "email": "testtest.com",
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
        make_course({"title": "course1", "section": 201, "designation": "CS351", "semester": "SP21"})

    def test_goodData(self):
        check = make_course({"title": "course0", "section": 200, "designation": "CS350", "semester": "SP21"})
        self.assertTrue(check, msg="Error: good course data fails to create course")
        self.assertEqual(len(CourseData.objects.all()), 2, msg="Error: new course is not created")

    def test_badData(self):
        check = make_course({"title": "course0", "section": "200"})
        self.assertFalse(check, msg="Error: making course does not fail when input is incorrect")
        self.assertFalse(CourseData.objects.filter(title="course0").exists(),
                         msg="Error: course data is stored when creation failed")

    def test_courseSectionExists(self):
        check = make_course({"title": "course1", "section": 201, "designation": "CS351"})
        self.assertFalse(check, msg="Error: making course does not fail when course section exists")
        tempCourse = CourseData.objects.get(designation__iexact="CS351")
        self.assertEqual(len(CourseSections.objects.filter(course=tempCourse, section=201)), 1,
                         msg="Error: extra section is created when data is incorrect")

    def test_existingCourse(self):
        check = make_course({"title": "course1", "section": 202, "designation": "CS351", "semester": " "})
        self.assertTrue(check, msg="Error: creating new section for a course fails when it should not")

    def test_missingData(self):
        check = make_course({"title": "course0"})
        self.assertFalse(check, msg="Error: making course does not fail if a section is not provided")

        check = make_course({"section": 201})
        self.assertFalse(check, msg="Error: making course does not fail when title is not provided")

    def test_makeSureItsWorking(self):
        course = CourseData(title="course2", designation="CS352")
        course.save()
        section = CourseSections(section=201, course=course)
        section.save()
        section = CourseSections(section=202, course=course)
        section.save()
        course = CourseData(title="course3", designation="CS353")
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
        self.tempCourse = CourseData(title="course1", id=1, designation="cs1")
        self.tempCourse.save()

    def test_goodData(self):
        check = make_lab({"designation": "cs1", "section": 801})
        self.assertTrue(check, msg="Error: creating a lab for a course that exists fails")
        query = list(LabData.objects.filter(course__title="course1"))
        self.assertEqual(len(query), 1, msg="Error: a single lab is not created for a course")
        self.assertEqual(query[0].section, 801, msg="Error: correct section is not created for the lab")

    def test_badData(self):
        check = make_lab({"designation": 1, "section": 801})
        self.assertFalse(check, msg="Error: bad course id does not fail")
        query = list(LabData.objects.filter(course__title="course1"))
        self.assertEqual(len(query), 0, msg="Error: a lab is created when courseId is bad")

        check = make_lab({"designation": "cs1", "section": "801"})
        self.assertFalse(check, msg="Error: bad section id does not fail")
        query = list(LabData.objects.filter(course__title="course1"))
        self.assertEqual(len(query), 0, msg="Error: a lab is created when section id is bad")

    def test_labExists(self):
        make_lab({"designation": "cs1", "section": 801})
        check = make_lab({"designation": "cs1", "section": 801})
        self.assertFalse(check, msg="Error: making a lab that already exists does not fail")
        query = list(LabData.objects.filter(course__title="course1"))
        self.assertEqual(len(query), 1, msg="Error: there is not exactly 1 lab section when identical data is passed")

    def test_courseDoesNotExist(self):
        check = make_lab({"designation": "cs2", "section": 801})
        self.assertFalse(check, msg="Error: making lab does not fail when course does not exist")
        query = list(LabData.objects.all())
        self.assertEqual(len(query), 0, msg="Error: a lab is created when coures does not exist")

    def test_missingData(self):
        check = make_lab({"section": 801})
        self.assertFalse(check, msg="Error: making lab does not fail when courseId is not given")
        query = list(LabData.objects.all())
        self.assertEqual(len(query), 0, msg="Error: a lab is created when coures is not provided")

        check = make_lab({"designation": "cs1"})
        self.assertFalse(check, msg="Error: making lab does not fail when section is not given")
        query = list(LabData.objects.all())
        self.assertEqual(len(query), 0, msg="Error: a lab is created when section is not given")

    def test_twoLabsOneCourse(self):
        make_lab({"designation": "cs1", "section": 801})
        check = make_lab({"designation": "cs1", "section": 802})
        self.assertTrue(check, msg="Error: making lab fails when labs for the same course have different sections")
        query = list(LabData.objects.all())
        self.assertEqual(len(query), 2, msg="Error: lab is not created when section is unique.")


class AssignTALabTest(TestCase):
    def setUp(self):
        tempCourse = CourseData.objects.create(title="course1", id=1, designation="cs1")
        self.lab = LabData.objects.create(course=tempCourse, section=801)
        self.ta = MyUser.objects.create(username="user1", position=UserType.TA)
        TAsToCourses.objects.create(TA=self.ta, course=tempCourse)
        self.notTa = MyUser.objects.create(username="user2", position=UserType.SUPERVISOR)

    def test_goodData(self):
        check = assign_ta_to_lab({"designation": "cs1", "labSection": 801, "taUsername": "user1"})
        print(check)
        self.assertTrue(check, msg="Error: good data does not return true for adding TA to lab")
        self.assertTrue(type(check) is bool, msg="Error: something other than a bool is returned on success")
        self.lab = LabData.objects.get(section=801)
        self.assertEqual(self.lab.TA, self.ta, msg="Error: wrong TA is assigned to lab")
        query = TAsToCourses.objects.all()
        self.assertEqual(len(query), 1, msg="Error: an object is not created in the linking table")
        self.assertEqual(query[0].TA, self.ta, msg="Error: wrong TA is created in linking table")
        self.assertEqual(query[0].course.title, "course1", msg="Error: wrong course is in the linking table")

    def test_badData(self):
        check = assign_ta_to_lab({"designation": 1, "labSection": 801, "taUsername": "user1"})
        self.assertFalse(check, msg="Error: bad data for assigning TA to lab does not fail")
        self.lab = LabData.objects.get(section=801)
        self.assertEqual(None, self.lab.TA, msg="Error: some TA is assigned to lab when bad data is passed")
        self.assertEqual(1, len(TAsToCourses.objects.all()), msg="Error: an extra entry is created in linking table")

        check = assign_ta_to_lab({"designation": "cs1", "labSection": "801", "taUsername": "user1"})
        self.assertFalse(check, msg="Error: bad data for assigning TA to lab does not fail")
        self.lab = LabData.objects.get(section=801)
        self.assertEqual(None, self.lab.TA, msg="Error: some TA is assigned to lab when bad data is passed")
        self.assertEqual(1, len(TAsToCourses.objects.all()), msg="Error: an extra entry is created in linking table")

        check = assign_ta_to_lab({"designation": "cs1", "labSection": 801, "taUsername": 1})
        self.assertFalse(check, msg="Error: bad data for assigning TA to lab does not fail")
        self.lab = LabData.objects.get(section=801)
        self.assertEqual(None, self.lab.TA, msg="Error: some TA is assigned to lab when bad data is passed")
        self.assertEqual(1, len(TAsToCourses.objects.all()), msg="Error: an extra entry is created in linking table")

    def test_taDoesNotExist(self):
        check = assign_ta_to_lab({"designation": "cs1", "labSection": 801, "taUsername": "user3"})
        self.assertFalse(check, msg="Error: when TA does not exist assigning TA does not return false")
        self.lab = LabData.objects.get(section=801)
        self.assertEqual(None, self.lab.TA, msg="Error: TA is assigned to lab when it should not be")

    def test_userNotTA(self):
        check = assign_ta_to_lab({"designation": "cs1", "labSection": 801, "taUsername": "user2"})
        self.assertFalse(check, msg="Error: trying to assign a supervisor as a TA does not fail")
        self.lab = LabData.objects.get(section=801)
        self.assertEqual(None, self.lab.TA, msg="Error: someone is assigned to lab when it should not be")

    def test_labDoesNotExist(self):
        check = assign_ta_to_lab({"designation": "cs1", "labSection": 802, "taUsername": "user1"})
        self.assertFalse(check, msg="Error: assigning TA does not fail when it should")
        self.lab = LabData.objects.get(section=801)
        self.assertEqual(None, self.lab.TA, msg="Error: TA is assigned to lab when it should not be")

    def test_missingData(self):
        check = assign_ta_to_lab({"labSection": 801, "taUsername": "user1"})
        self.assertFalse(check, msg="Error: missing data for assigning TA to lab does not fail")
        self.lab = LabData.objects.get(section=801)
        self.assertEqual(None, self.lab.TA, msg="Error: some TA is assigned to lab when bad data is passed")
        self.assertEqual(1, len(TAsToCourses.objects.all()), msg="Error: an extra entry is created in linking table")

        check = assign_ta_to_lab({"designation": "cs1", "taUsername": "user1"})
        self.assertFalse(check, msg="Error: bad data for assigning TA to lab does not fail")
        self.lab = LabData.objects.get(section=801)
        self.assertEqual(None, self.lab.TA, msg="Error: some TA is assigned to lab when bad data is passed")
        self.assertEqual(1, len(TAsToCourses.objects.all()), msg="Error: an extra entry is created in linking table")

        check = assign_ta_to_lab({"designation": "cs1", "labSection": 801})
        self.assertFalse(check, msg="Error: bad data for assigning TA to lab does not fail")
        self.lab = LabData.objects.get(section=801)
        self.assertEqual(None, self.lab.TA, msg="Error: some TA is assigned to lab when bad data is passed")
        self.assertEqual(1, len(TAsToCourses.objects.all()), msg="Error: an extra entry is created in linking table")


class AssignTAToCourseTest(TestCase):
    def setUp(self):
        CourseData.objects.create(title="course1", id=1, designation="cs1")
        self.ta = MyUser.objects.create(username="user1", position=UserType.TA)
        self.notTa = MyUser.objects.create(username="user2", position=UserType.SUPERVISOR)

    def test_goodData(self):
        check = assign_ta_to_course({"designation": "cs1", "taUsername": "user1"})
        self.assertTrue(check, msg="Error: good data does not assign ta to course")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(1, len(query), msg="Error: not 1 object is created in the linking database")
        self.assertEqual(query[0].TA, self.ta, msg="Error: wrong TA is in the linking database")
        self.assertEqual(query[0].course.title, "course1", msg="Error: wrong course is in the linking database")

    def test_badData(self):
        check = assign_ta_to_course({"designation": 1, "taUsername": "user1"})
        self.assertFalse(check, msg="Error: bad data does not return false")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(0, len(query), msg="Error: an object was created in the linking database")

        check = assign_ta_to_course({"designation": "cs1", "taUsername": 1})
        self.assertFalse(check, msg="Error: bad data does not return false")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(0, len(query), msg="Error: an object was created in the linking database")

    def test_userNotTA(self):
        check = assign_ta_to_course({"designation": "cs1", "taUsername": "user2"})
        self.assertFalse(check, msg="Error: when given a non-TA's username, assigning a TA does not fail")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(0, len(query), msg="Error: an object was created in the linking database")

    def test_userNotExist(self):
        check = assign_ta_to_course({"designation": "cs1", "taUsername": "user3"})
        self.assertFalse(check, msg="Error: nonexistent user does not return false")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(0, len(query), msg="Error: an object was created in the linking database")

    def test_courseNotExist(self):
        check = assign_ta_to_course({"designation": "cs2", "taUsername": "user1"})
        self.assertFalse(check, msg="Error: does not return false when course does not exist")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(0, len(query), msg="Error: an object was created in the linking database")

    def test_alreadyAssigned(self):
        assign_ta_to_course({"designation": "cs1", "taUsername": "user1"})
        check = assign_ta_to_course({"designation": "cs1", "taUsername": "user1"})
        self.assertFalse(check, msg="Error: assigning already assigned TA does not return false")
        query = list(TAsToCourses.objects.all())
        self.assertEqual(1, len(query), msg="Error: an extra object was created in the linking database")


class AssignInstructorCourseTest(TestCase):
    def setUp(self):
        tempCourse = CourseData(title="course1", id=1, designation="cs1")
        tempCourse.save()
        CourseSections.objects.create(course=tempCourse, section=201)
        CourseSections.objects.create(course=tempCourse, section=202)
        MyUser.objects.create(username="user1", position=UserType.INSTRUCTOR)
        MyUser.objects.create(username="user2", position=UserType.TA)

    def test_goodData(self):
        check = assign_instructor({"designation": "cs1", "courseSection": 201, "instructorUsername": "user1"})
        self.assertTrue(check, msg="Error: good data does not return true")
        section = CourseSections.objects.get(course_id=1, section=201)
        instruct = MyUser.objects.get(username="user1")
        self.assertEqual(section.instructor, instruct, msg="Error: wrong instructor assigned")
        section = CourseSections.objects.get(course_id=1, section=202)
        self.assertEqual(section.instructor, None, msg="Error: instructor was assigned to the wrong course")

    def test_badData(self):
        check = assign_instructor({"designation": 1, "courseSection": 201, "instructorUsername": "user1"})
        self.assertFalse(check, msg="Error: wrong input type does not return false")
        check = assign_instructor({"designation": "cs1", "courseSection": "201", "instructorUsername": "user1"})
        self.assertFalse(check, msg="Error: wrong input type does not return false")
        check = assign_instructor({"designation": "cs1", "courseSection": 201, "instructorUsername": 1})
        self.assertFalse(check, msg="Error: non-instructor does not return false")

        sections = list(CourseSections.objects.filter(course_id=1))
        for i in sections:
            self.assertEqual(i.instructor, None, msg="Error: an instructor was assigned to course " + str(i.id))

    def test_userNotInstructor(self):
        check = assign_instructor({"designation": "cs1", "courseSection": 201, "instructorUsername": "user2"})
        self.assertFalse(check, msg="Error: non-instructor does not return false")
        section = CourseSections.objects.get(course_id=1, section=201)
        self.assertEqual(section.instructor, None,
                         msg="Error: someone was assigned to the course when a non-instructor was provided")

    def test_courseDoesNotExist(self):
        check = assign_instructor({"designation": "cs2", "courseSection": 201, "instructorUsername": "user1"})
        self.assertFalse(check, msg="Error: missing course does not return false")
        sections = list(CourseSections.objects.filter(course_id=1))
        for i in sections:
            self.assertEqual(i.instructor, None, msg="Error: an instructor was assigned to course " + str(i.id))

    def test_instructorDoesNotExist(self):
        check = assign_instructor({"designation": "cs1", "courseSection": 201, "instructorUsername": "user3"})
        self.assertFalse(check, msg="Error: missing user does not return false")
        sections = list(CourseSections.objects.filter(course_id=1))
        for i in sections:
            self.assertEqual(i.instructor, None, msg="Error: an instructor was assigned to course " + str(i.id))

    def test_missingData(self):
        check = assign_instructor({"designation": "cs1", "courseSection": 201})
        self.assertFalse(check, msg="Error: missing username does not return false")

        check = assign_instructor({"designation": "cs1", "instructorUsername": "user1"})
        self.assertFalse(check, msg="Error: missing course section does not return false")

        check = assign_instructor({"courseSection": 201, "instructorUsername": "user1"})
        self.assertFalse(check, msg="Error: missing courseId does not return false")

        sections = list(CourseSections.objects.filter(course_id=1))
        for i in sections:
            self.assertEqual(i.instructor, None, msg="Error: an instructor was assigned to course " + str(i.id))

    def test_assignAll(self):
        check = assign_instructor({"designation": "cs1", "instructorUsername": "user1"}, all=True)
        self.assertTrue(check, msg="Error: assigning instructor to all sections fails.")
        tempUser = MyUser.objects.get(username="user1")
        sections = list(CourseSections.objects.all())
        for i in sections:
            self.assertEqual(i.instructor, tempUser, msg="Error: instructor is not assigned to a section")


class GetCourseIDTest(TestCase):
    def setUp(self):
        for i in range(5):
            CourseData.objects.create(title="course" + str(i), id=i * 2, designation="CS" + str(i))

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
    def setUp(self):
        MyUser.objects.create(username="user1", email="originalemail1", addressln1="3400 N Maryland",
                              phone_number="123456789")
        MyUser.objects.create(username="user2", email="originalemail2", addressln1="3401 N Maryland",
                              phone_number="987654321")

    def test_goodData(self):
        check = update_user(
            {"username": "user1", "email": "newemail1", "addressln1": "3400 S Maryland", "phone_number": "100200300"})
        self.assertTrue(check, msg="Error: updating user does not return true when data is good")
        user = MyUser.objects.get(username="user1")
        self.assertEqual(user.email, "newemail1", msg="Error: email is not updated")
        self.assertEqual(user.addressln1, "3400 S Maryland", msg="Error: address is not updated")
        self.assertEqual(user.phone_number, "100200300", msg="Error: phone number is not updated")

    def test_userNoExist(self):
        check = update_user(
            {"username": "user3", "email": "newemail1", "addressln1": "3400 S Maryland", "phone_number": "100200300"})
        self.assertFalse(check, msg="Error: check does not return false when user does not exist")

    def test_invalidData(self):
        check = update_user(
            {"username": 1, "email": "newemail1", "addressln1": "3400 S Maryland", "phone_number": "100200300"})
        self.assertFalse(check, msg="Error: updating user does not return false when username is incorrect type")
        check = update_user(
            {"username": "user1", "email": 1, "addressln1": "3400 S Maryland", "phone_number": "100200300"})
        self.assertFalse(check, msg="Error: updating user does not return false when email is incorrect type")
        check = update_user({"username": "user1", "email": "newemail1", "addressln1": 1, "phone_number": "100200300"})
        self.assertFalse(check, msg="Error: updating user does not return false when address is incorrect type")
        check = update_user(
            {"username": "user1", "email": 1, "addressln1": "3400 S Maryland", "phone_number": 100200300})
        self.assertFalse(check, msg="Error: updating user does not return false when phone number is incorrect type")

    def test_updateSome(self):
        check = update_user({"username": "user1", "email": "newemail1"})
        self.assertTrue(check, msg="Error: updating user does not succeed when only updating email")
        user = MyUser.objects.get(username="user1")
        self.assertEqual(user.email, "newemail1", msg="Error: email is not updated")
        self.assertEqual(user.addressln1, "3400 N Maryland", msg="Error: address is erroneously updated")
        self.assertEqual(user.phone_number, "123456789", msg="Error: phone number is erroneously updated")
        check = update_user({"username": "user1", "addressln1": "new address"})
        self.assertTrue(check, msg="Error: updating user does not succeed when only updating address")
        user = MyUser.objects.get(username="user1")
        self.assertEqual(user.email, "newemail1", msg="Error: email is updated when it should not be")
        self.assertEqual(user.addressln1, "new address", msg="Error: address is not updated")
        self.assertEqual(user.phone_number, "123456789", msg="Error: phone number is erroneously updated")


class ListCoursesTest(TestCase):
    def setUp(self):
        self.result = []

        for i in range(1, 11):
            temp = CourseData.objects.create(title="course" + str(i), designation="CS" + str(i), id=i)
            temptup = (str(temp), "CS" + str(i), [], [])
            for j in range(1, 4):
                temptup[2].append(str(CourseSections.objects.create(course=temp, section=(j + 200))))
            for j in range(1, 4):
                temptup[3].append(str(LabData.objects.create(course=temp, section=(j + 900))))
            self.result.append(temptup)

        print(self.result)

    def test_good(self):
        alldata = list(list_courses())
        self.assertListEqual(alldata, self.result, msg="Error")


class ListUsersTest(TestCase):
    def setUp(self):
        self.users = []
        for i in range(1, 11):
            tempFn = "john" + str(i)
            tempLn = "doe" + str(i)
            tempUser = "user" + str(i)
            self.users.append((tempFn + " " + tempLn, str(UserType.TA), tempUser))
            MyUser.objects.create(username=tempUser, first_name=tempFn, last_name=tempLn, position=UserType.TA)
        for i in range(11, 21):
            tempFn = "john" + str(i)
            tempLn = "doe" + str(i)
            tempUser = "user" + str(i)
            self.users.append((tempFn + " " + tempLn, str(UserType.SUPERVISOR), tempUser))
            MyUser.objects.create(username=tempUser, first_name=tempFn, last_name=tempLn, position=UserType.SUPERVISOR)
        for i in range(21, 31):
            tempFn = "john" + str(i)
            tempLn = "doe" + str(i)
            tempUser = "user" + str(i)
            self.users.append((tempFn + " " + tempLn, str(UserType.INSTRUCTOR), tempUser))
            MyUser.objects.create(username=tempUser, first_name=tempFn, last_name=tempLn, position=UserType.INSTRUCTOR)

    def test_good(self):
        self.assertListEqual(list_users(), self.users, msg="Error: listusers is wrong.")


class ListInstructorsTest(TestCase):
    def setUp(self):
        self.instructors = []
        for i in range(1, 11):
            tempFn = "john" + str(i)
            tempLn = "doe" + str(i)
            tempUser = "user" + str(i)
            MyUser.objects.create(username=tempUser, first_name=tempFn, last_name=tempLn, position=UserType.TA)
        for i in range(11, 21):
            tempFn = "john" + str(i)
            tempLn = "doe" + str(i)
            tempUser = "user" + str(i)
            MyUser.objects.create(username=tempUser, first_name=tempFn, last_name=tempLn, position=UserType.SUPERVISOR)
        for i in range(21, 31):
            tempFn = "john" + str(i)
            tempLn = "doe" + str(i)
            tempUser = "user" + str(i)
            self.instructors.append((tempFn + " " + tempLn, tempUser))
            MyUser.objects.create(username=tempUser, first_name=tempFn, last_name=tempLn, position=UserType.INSTRUCTOR)

    def test_listInstructors(self):
        instructors = list(list_instructors())
        self.assertListEqual(instructors, self.instructors, msg="Error: generated list of instructors is incorrect")


class ListTAsTest(TestCase):
    def setUp(self):
        self.tas = []
        for i in range(1, 11):
            tempFn = "john" + str(i)
            tempLn = "doe" + str(i)
            tempUser = "user" + str(i)
            self.tas.append((tempFn + " " + tempLn, tempUser))
            MyUser.objects.create(username=tempUser, first_name=tempFn, last_name=tempLn, position=UserType.TA)
        for i in range(11, 21):
            tempFn = "john" + str(i)
            tempLn = "doe" + str(i)
            tempUser = "user" + str(i)
            MyUser.objects.create(username=tempUser, first_name=tempFn, last_name=tempLn, position=UserType.SUPERVISOR)
        for i in range(21, 31):
            tempFn = "john" + str(i)
            tempLn = "doe" + str(i)
            tempUser = "user" + str(i)
            MyUser.objects.create(username=tempUser, first_name=tempFn, last_name=tempLn, position=UserType.INSTRUCTOR)

    def test_listTAs(self):
        tas = list(list_tas())
        self.assertListEqual(tas, self.tas, msg="Error: generated list of TAs is incorrect")


class TestGetUserdata(TestCase):
    def setUp(self):
        MyUser.objects.create(username="user1", first_name="John", last_name="Doe", addressln1="address",
                              addressln2="more address", email="tst@test.com", phone_number="123456")
        MyUser.objects.create(username="user2", first_name="John2", last_name="Doe2", addressln1="address2",
                              addressln2="more address2", email="tst2@test.com", phone_number="1234562")

    def test_getUserdata(self):
        needToReturn = ["username", "first_name", "last_name", "addressln1", "addressln2", "email", "phone_number"]
        data = get_userdata("user1")
        self.assertTrue(data, msg="Error: existing user does not return a truthy dictionary")
        self.assertTrue(isinstance(data, dict), msg="Error: a dict is not returned")
        self.assertListEqual(list(data.keys()), needToReturn,
                             msg="Error: the right items are not included in the returned dictionary")
        self.assertEqual(data['first_name'], "John", msg="Error: first name is wrong")
        self.assertEqual(data['last_name'], "Doe", msg="Error: last name is wrong")

    def test_getUserNotExist(self):
        data = get_userdata("user3")
        self.assertFalse(data, msg="Error: getting data of user who does not exist does not fail")
        self.assertTrue(isinstance(data, ErrorString), msg="Error: an ErrorString is not returned")

    def test_getUserBadInput(self):
        data = get_userdata(1)
        self.assertFalse(data, msg="Error: getting data of user with bad input does not fail")
        self.assertTrue(isinstance(data, ErrorString), msg="Error: an ErrorString is not returned")


class TestGetCourseData(TestCase):
    def setUp(self):
        for i in range(5):
            title = "course " + str(i)
            designation = "CS" + str(i)
            semester = "SP21"
            course = CourseData.objects.create(title=title, designation=designation, semester=semester)
            for j in range(i):
                section = 201 + j
                CourseSections.objects.create(course=course, section=section)
            for j in range(i):
                section = 901 + j
                LabData.objects.create(course=course, section=section)

    def test_getCourseData(self):
        toReturn = ["designation", "title", "sections", "labs", "semester"]
        for i in range(5):
            course = get_coursedata("CS" + str(i))
            self.assertEqual(list(course.keys()), toReturn,
                             msg="Error: returned dictionary does not contain the right keys")
            self.assertEqual(course['title'], "course " + str(i), msg="Error: returned course title is wrong")
            self.assertEqual(course['designation'], "CS" + str(i), msg="Error: returned designation is incorrect")
            self.assertEqual(len(course['sections']), i,
                             msg="Error: returned list of course sections does not contain the right number of sections")
            self.assertEqual(len(course['labs']), i,
                             msg="Error: returned list of course labs does not contain the right number of labs")


class TestGetTAsOfCourse(TestCase):
    def setUp(self):
        tas = []
        self.numCourses = 5
        for i in range(self.numCourses):
            username = "user" + str(i)
            first_name = "john" + str(i)
            last_name = "doe" + str(i)
            tas.append(MyUser.objects.create(username=username, first_name=first_name, last_name=last_name))

        for i in range(self.numCourses):
            title = "course " + str(i)
            designation = "CS" + str(i)
            semester = "SP21"
            course = CourseData.objects.create(title=title, designation=designation, semester=semester)
            for j in range(i):
                TAsToCourses.objects.create(TA=tas[j], course=course)

    def test_getTAsOfCourse(self):
        for i in range(self.numCourses):
            tas = list(get_tas_of_course("CS" + str(i)))
            self.assertEqual(len(tas), i, msg="Error: wrong number of TAs assigned to a course returned.")
            for j in range(i):
                self.assertEqual(("john" + str(j) + " doe" + str(j), "user" + str(j)), tas[j],
                                 msg="Error: wrong ta is in list")

    def test_getTAsOfNonExistingCourse(self):
        tas = get_tas_of_course("CS-1")
        self.assertFalse(tas, msg="Error: when course does not exist getting tas of the course does not fail")

    def test_getTAsOfCourseBadInput(self):
        tas = get_tas_of_course(2)
        self.assertFalse(tas, msg="Error: calling get tas of course does not fail when input is bad")


class TestGetInstructorsCourses(TestCase):
    def setUp(self):
        instructors = []
        self.numCourses = 5
        for i in range(self.numCourses):
            username = "instructor" + str(i)
            first_name = "john" + str(i)
            last_name = "doe" + str(i)
            instructors.append(
                MyUser.objects.create(username=username, first_name=first_name, last_name=last_name, position="I"))

        for i in range(self.numCourses):
            title = "course " + str(i)
            designation = "CS" + str(i)
            semester = "SP21"
            course = CourseData.objects.create(title=title, designation=designation, semester=semester)
            for j in range(i):
                section = 200 + j
                CourseSections.objects.create(course=course, instructor=instructors[j], section=section)

    def test_getInstructorsCourses(self):
        print(list(list_courses()))
        for i in range(self.numCourses):
            courses = get_courses_of_instructor("instructor" + str(i))
            self.assertEqual(len(courses), self.numCourses - i - 1,
                             msg="Error: incorrect number of courses assigned to an instructor is returned")

    def test_instructorAssignedToMultipleSectionsOfSameCourse(self):
        inst0 = MyUser.objects.get(username="instructor1")
        course1 = CourseData.objects.get(designation="CS1")
        CourseSections.objects.create(course=course1, instructor=inst0, section=999)
        courses = get_courses_of_instructor("instructor1")
        self.assertEqual(len(courses), 4, msg="Error: wrong number of courses for an instructor is returned")

    def test_userIsNotInstructor(self):
        MyUser.objects.create(username="notinstructor", position="T")
        courses = get_courses_of_instructor("notinstructor")
        self.assertFalse(courses, msg="Error: trying to get the courses of a TA does not fail")
        MyUser.objects.create(username="Supervisor", position="S")
        courses = get_courses_of_instructor("Supervisor")
        self.assertFalse(courses, msg="Error: trying to get the courses of a supervisor does not fail")


    def test_userDoesNotExist(self):
        courses = get_courses_of_instructor("thisisnotauser")
        self.assertFalse(courses, msg="Error: trying to get the courses of a user who does not exist does not fail")


class TestGetAllUserInfo(TestCase):
    def setUp(self):
        pass

    def test_getAllUserInfoNonSupervisor(self):
        check = get_all_user_info()

    def test_getAllUserInfoSuervisor(self):
        check = get_all_user_info(True)


class TestGetSkills(TestCase):
    def setUp(self):
        pass

    def test_getSkills(self):
        check = get_skills("ta1")


class TestUpdateSkill(TestCase):
    def setUp(self):
        pass

    def test_updateSkill(self):
        check = update_ta_skill({"taUsername": "ta1", "skills": "here are my skills"})


class TestDeleteAccount(TestCase):
    def setUp(self):
        pass

    def test_deleteAccount(self):
        check = delete_account("user1")
