from .models import MyUser, UserType, CourseData, LabData, TAsToCourses


class ErrorString():
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

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
    """creates a course in the database according to the given input. On success, returns False, on failure returns
    string describing error"""
    if not coursedata.get("title"):
        return ErrorString("Error: title is not provided in coursedata")

    if CourseData.objects.filter(title = coursedata["title"]).exists():
        return ErrorString("Error: course with title " + coursedata["title"] + " already exists")

    tempCourse = CourseData(title=coursedata["title"])
    tempCourse.save()

    return False


def login(logindata):
    """handles interacting with the database for logging in. Returns false on failure, or a dictionary of first and last name and position on success"""
    pass


def make_lab():
    pass

