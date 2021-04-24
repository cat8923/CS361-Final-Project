from .models import MyUser, UserType, CourseData, LabData, TAsToCourses, CourseSections


class ErrorString():
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message

    def __bool__(self):
        return False


def verify_dict(needed, toVerify: dict):
    for i in needed:
        if not toVerify.get(i[0]):
            return ErrorString("Error: " + i[0] + " was not provided")
        if type(toVerify[i[0]]) is not i[1]:
            return ErrorString("Error: invalid datatype for " + i[0])

    return True


def make_user(userdata: dict):
    """creates a user in the database according to the given information. On success, returns True on failure returns an
    ErrorString describing the error."""
    needed = [("username", str), ("password", str), ("first_name", str), ("last_name", str), ("address", str), ("title", UserType), ("email", str), ("number", str)]
    check = verify_dict(needed, userdata)
    if not check:
        return check
    #for i in needed:
    #    if not userdata.get(i[0]):
    #        return ErrorString("Error: " + i[0] + " was not provided in userdata")
    #    if type(userdata[i[0]]) is not i[1]:
    #        return ErrorString("Error: invalid " + i[0])

    if MyUser.objects.filter(username=userdata["username"]).exists():
        return ErrorString("Error: username " + userdata["username"] + " is already taken")

    tempUser = MyUser(username=userdata["username"], first_name=userdata["first_name"], last_name=userdata["last_name"],
                      address=userdata["address"], position=userdata["title"], phone_number=userdata["number"],
                      email=userdata["email"])
    tempUser.set_password(userdata["password"])
    tempUser.save()

    return True


def update_user(userdata: dict):
    """updates a given user based off of the given information"""
    pass


def make_course(coursedata: dict):
    """creates a course in the database according to the given input. On success, returns True, on failure returns
    string describing error.
    Note: this method does not handle assigning instructors; use the assign_instructor method instead."""
    needed = [("title", str), ("section", int)]
    if not coursedata.get("title"):
        return ErrorString("Error: title is not provided in coursedata")
    if not type(coursedata["title"]) is str:
        return ErrorString("Error: wrong type for course title")

    if not coursedata.get("section"):
        return ErrorString("Error: section is not provided in coursedata")
    if not type(coursedata["section"]) is int:
        return ErrorString("Error: wrong type for section")

    if CourseSections.objects.filter(course__title__iexact=coursedata["title"], section=coursedata["section"]).exists():
        return ErrorString("Error: course with title " + coursedata["title"] + "and section " + str(coursedata["section"]) + " already exists")

    tempCourse = CourseData.objects.filter(title=coursedata["title"])
    print(list(map(str, tempCourse)))

    if not tempCourse:
        tempCourse = CourseData(title=coursedata["title"])
        tempCourse.save()
    else:
        tempCourse = tempCourse[0]

    tempSection = CourseSections(course=tempCourse, section=coursedata["section"])
    tempSection.save()

    return True


def login(logindata: dict):
    """handles interacting with the database for logging in. Returns ErrorString (False) on failure, or a dictionary of
    first and last name and position on success"""
    needed = [("username", str), ("password", str)]
    check = verify_dict(needed, logindata)
    if not check:
        return check
    #for i in needed:
    #    if not logindata.get(i):
    #        return ErrorString("Error: " + i + " not provided")
    #    if not type(logindata[i]) is str:
    #        return ErrorString("Error: bad input data")

    tempUser = MyUser.objects.filter(username=logindata["username"]).exists()
    if not tempUser:
        return ErrorString("Error: user does not exist")

    tempUser = MyUser.objects.get(username=logindata["username"])
    if not tempUser.check_password(raw_password=logindata["password"]):
        return ErrorString("Error: incorrect password")

    return {"first_name": tempUser.first_name, "last_name": tempUser.last_name, "position": tempUser.position}


def make_lab(labdata: dict):
    """handles making a lab given the user lab data. On failure, return ErrorString describing error. On success, return True"""
    needed = [("courseId", int), ("section", int)]
    check = verify_dict(needed, labdata)
    if not check:
        return check

    if LabData.objects.filter(course_id=labdata["courseId"], section=labdata["section"]).exists():
        return ErrorString("Error: lab section for this course already exists")

    query = CourseData.objects.filter(id=labdata["courseId"])
    if not query.exists():
        return ErrorString("Error: course does not exist")

    LabData.objects.create(course=(list(query))[0], section=labdata["section"])
    return True


def assign_ta_to_lab(data: dict):
    """handles assigning a ta to a lab. Will also assign the TA to a course On failure returns ErrorString describing error. On success, returns true"""
    needed = [("courseId", int), ("labSection", int), ("taUsername", str)]
    check = verify_dict(needed, data)
    if not check:
        return check

    query = list(LabData.objects.filter(course_id=data["courseId"], section=data["labSection"]))
    if len(query) is 0:
        return ErrorString("Error: lab section does not exist")

    tempLab = query[0]

    query = list(MyUser.objects.filter(username__iexact=data["taUsername"]))
    if len(query) is 0:
        return ErrorString("Error: user does not exist")

    tempUser = query[0]

    if tempUser.position is not str(UserType.TA):
        return ErrorString("Error: user is not a TA")

    tempLab.TA = tempUser
    tempLab.save()

    assign_ta_to_course(data)

    return True


def assign_ta_to_course(data: dict):
    """handles assigning a ta to a course without assigning to a particular lab section."""
    needed = [("courseId", int), ("taUsername", str)]
    check = verify_dict(needed, data)
    if not check:
        return check

    query = list(CourseData.objects.filter(id=data["courseId"]))
    if len(query) is 0:
        return ErrorString("Error: course does not exist")

    tempCourse = query[0]

    query = list(MyUser.objects.filter(username__iexact=data["taUsername"]))
    if len(query) is 0:
        return ErrorString("Error: user does not exist")

    if query[0].position is not str(UserType.TA):
        return ErrorString("Error: user is not a TA")

    tempUser = query[0]

    if TAsToCourses.objects.filter(TA=tempUser, course=tempCourse).exists():
        return ErrorString("Error: TA has already been assigned to course")

    TAsToCourses.objects.create(TA=tempUser, course=tempCourse)

    return True


def assign_instructor(data: dict):
    """handles assigning an instructor to a course section in the given data. On failure returns ErrorString describing error.
    On success, returns True. Warning: will override an existing instructor of a course"""
    needed = [("courseId", int), ("courseSection", int), ("instructorUsername", str)]
    check = verify_dict(needed, data)
    if not check:
        return check

    query = list(CourseSections.objects.filter(course_id=data["courseId"], section=data["courseSection"]))
    if not query:
        return ErrorString("Error: course section not found")

    tempSection = query[0]

    query = list(MyUser.objects.filter(username=data["instructorUsername"]))
    if not query:
        return ErrorString("Error: user not found")

    tempUser = query[0]

    if tempUser.position is not str(UserType.INSTRUCTOR):
        return ErrorString("Error: user is not an instructor")

    tempSection.instructor = tempUser
    tempSection.save()

    return True


def get_course_id_by_name(courseName: str):
    """gets the id of a course by its name (case insensitive). Returns the id on success, or an ErrorString saying
    whether the course did not exist or if data were invalid"""
    if type(courseName) is not str:
        return ErrorString("Error: incorrect data")

    if not CourseData.objects.filter(title__iexact=courseName).exists():
        return ErrorString("Error: course does not exist")

    return CourseData.objects.get(title__iexact=courseName).id


def list_courses() -> list:
    pass


def list_users() -> list:
    pass
