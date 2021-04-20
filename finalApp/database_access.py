from .models import MyUser, UserType, CourseData, LabData, TAsToCourses, CourseSections


class ErrorString():
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message

    def __bool__(self):
        return False


def make_user(userdata):
    """creates a user in the database according to the given information. On success, returns True on failure returns an
    ErrorString describing the error."""
    needed = ["username", "password", "first_name", "last_name", "address", "title", "email", "number"]
    for i in needed:
        if not userdata.get(i):
            return ErrorString("Error: " + i + " was not provided in userdata")

    if MyUser.objects.filter(username=userdata["username"]).exists():
        return ErrorString("Error: username " + userdata["username"] + " is already taken")

    tempUser = MyUser(username=userdata["username"], first_name=userdata["first_name"], last_name=userdata["last_name"],
                      address=userdata["address"], position=userdata["title"], phone_number=userdata["number"],
                      email=userdata["email"])
    tempUser.set_password(userdata["password"])
    tempUser.save()

    return True


def make_course(coursedata):
    """creates a course in the database according to the given input. On success, returns True, on failure returns
    string describing error.
    Note: this method does not handle assigning instructors; use the assign_instructor method instead."""
    if not coursedata.get("title"):
        return ErrorString("Error: title is not provided in coursedata")

    if not coursedata.get("section"):
        return ErrorString("Error: section is not provided in coursedata")

    if CourseSections.objects.filter(course__title=coursedata["title"], section=coursedata["section"]).exists():
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


def login(logindata):
    """handles interacting with the database for logging in. Returns ErrorString (False) on failure, or a dictionary of
    first and last name and position on success"""
    pass


def make_lab(labdata):
    """handles making a lab given the user lab data. On failure, return ErrorString describing error. On success, return True"""
    pass


def assign_ta(data):
    """handles assigning a ta to a course. On failure returns ErrorString describing error. On success, returns true"""
    pass


def assign_instructor(data):
    """handles assigning an instructor to a course in the given data. On failure returns ErrorString describing error.
    On success, returns True."""
    pass


def get_course_id_by_name(courseName):
    """gets the id of a course by its name (case insensitive). Returns the id on success, or an ErrorString saying
    whether the course did not exist or if data were invalid"""
    pass
