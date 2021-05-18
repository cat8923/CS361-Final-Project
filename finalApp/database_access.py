
from .models import MyUser, UserType, CourseData, LabData, TAsToCourses, CourseSections, TASkills
from typing import Union

class ErrorString():
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message

    def __bool__(self):
        return False


def verify_dict(needed: list[(str, type)], toVerify: dict) -> Union[ErrorString, bool]:
    for i in needed:
        if not toVerify.get(i[0]):
            return ErrorString("Error: " + i[0] + " was not provided")
        if type(toVerify[i[0]]) is not i[1]:
            return ErrorString("Error: invalid datatype for " + i[0])

    return True


def make_user(userdata: dict) -> Union[ErrorString, bool]:
    """creates a user in the database according to the given information. On success, returns True on failure returns an
    ErrorString describing the error."""
    needed = [("username", str), ("password", str), ("first_name", str), ("last_name", str), ("addressln1", str), ("addressln2", str),("title", str), ("email", str), ("number", str)]
    check = verify_dict(needed, userdata)
    if not check:
        return check

    if MyUser.objects.filter(username__iexact=userdata["username"]).exists():
        return ErrorString("Error: username " + userdata["username"] + " is already taken")

    tempUser = MyUser(username=userdata["username"], first_name=userdata["first_name"], last_name=userdata["last_name"],
                      addressln1=userdata["addressln1"], addressln2=userdata["addressln2"], position=userdata["title"], phone_number=userdata["number"],
                      email=userdata["email"])
    tempUser.set_password(userdata["password"])
    tempUser.save()

    return True


def update_user(userdata: dict) -> Union[ErrorString, bool]:
    """updates a given user based off of the given information
    Possible information to update: email, address, phone number"""
    toUpdate = []
    if "username" not in userdata:
        return ErrorString("Error: username must be provided")
    maybeNeeded = [("email", str), ("addressln1", str), ("addressln2", str), ("phone_number", str), ("first_name", str), ("last_name", str)] # makes it very easy if we need to add more things to update
    for i in maybeNeeded:
        if i[0] in userdata:
            if type(userdata[i[0]]) is not i[1]:
                return ErrorString("Error: wrong datatype provided for " + i[0])
            toUpdate.append(i[0])

    user = list(MyUser.objects.filter(username__iexact=userdata["username"]))
    if not user:
        return ErrorString("Error: user not found")
    user = user[0]

    for i in toUpdate:
        setattr(user, i, userdata[i])

    user.save()

    return True


def make_course(coursedata: dict) -> Union[ErrorString, bool]:
    """creates a course in the database according to the given input. On success, returns True, on failure returns
    string describing error.
    Note: this method does not handle assigning instructors; use the assign_instructor method instead."""
    needed = [("title", str), ("section", int), ("designation", str), ("semester", str)]
    check = verify_dict(needed, coursedata)
    if not check:
        return check

    if CourseSections.objects.filter(course__designation__iexact=coursedata["designation"], section=coursedata["section"]).exists():
        return ErrorString("Error: course with title " + coursedata["title"] + "and section " + str(coursedata["section"]) + " already exists")

    tempCourse = CourseData.objects.filter(designation__iexact=coursedata["designation"])
    print(list(map(str, tempCourse)))

    if not tempCourse:
        tempCourse = CourseData(title=coursedata["title"], designation=coursedata["designation"], semester=coursedata["semester"])
        tempCourse.save()
    else:
        tempCourse = tempCourse[0]

    tempSection = CourseSections(course=tempCourse, section=coursedata["section"])
    tempSection.save()

    return True


def login(logindata: dict) -> Union[ErrorString, dict]:
    """handles interacting with the database for logging in. Returns ErrorString (False) on failure, or a dictionary of
    first and last name and position and username on success"""
    needed = [("username", str), ("password", str)]
    check = verify_dict(needed, logindata)
    if not check:
        return check

    tempUser = MyUser.objects.filter(username__iexact=logindata["username"]).exists()
    if not tempUser:
        return ErrorString("Error: bad username or password")

    tempUser = MyUser.objects.get(username__iexact=logindata["username"])
    if not tempUser.check_password(raw_password=logindata["password"]):
        return ErrorString("Error: bad username or password")

    return {"first_name": tempUser.first_name, "last_name": tempUser.last_name, "position": tempUser.position}


def make_lab(labdata: dict) -> Union[ErrorString, bool]:
    """handles making a lab given the user lab data. On failure, return ErrorString describing error. On success, return True"""
    needed = [("designation", str), ("section", int)]
    check = verify_dict(needed, labdata)
    if not check:
        return check

    if LabData.objects.filter(course__designation__iexact=labdata["designation"], section=labdata["section"]).exists():
        return ErrorString("Error: lab section for this course already exists")

    query = CourseData.objects.filter(designation__iexact=labdata["designation"])
    if not query.exists():
        return ErrorString("Error: course does not exist")

    LabData.objects.create(course=(list(query))[0], section=labdata["section"])
    return True


def assign_ta_to_lab(data: dict) -> Union[ErrorString, bool]:
    """handles assigning a ta to a lab. On failure returns ErrorString describing error. On success, returns true"""
    needed = [("designation", str), ("labSection", int), ("taUsername", str)]
    check = verify_dict(needed, data)
    if not check:
        return check

    query = list(LabData.objects.filter(course__designation__iexact=data["designation"], section=data["labSection"]))
    if len(query) == 0:
        return ErrorString("Error: lab section does not exist")

    tempLab = query[0]

    query = list(MyUser.objects.filter(username__iexact=data["taUsername"]))
    if len(query) == 0:
        return ErrorString("Error: user does not exist")

    tempUser = query[0]

    if tempUser.position != str(UserType.TA):
        return ErrorString("Error: user is not a TA")

    if not TAsToCourses.objects.filter(TA=tempUser, course=tempLab.course).exists():
        return ErrorString("Error: TA is not assigned to course.")

    tempLab.TA = tempUser
    tempLab.save()

    return True


def assign_ta_to_course(data: dict) -> Union[ErrorString, bool]:
    """handles assigning a ta to a course without assigning to a particular lab section."""
    needed = [("designation", str), ("taUsername", str)]
    check = verify_dict(needed, data)
    if not check:
        return check

    query = list(CourseData.objects.filter(designation__iexact=data["designation"]))
    if len(query) == 0:
        return ErrorString("Error: course does not exist")

    tempCourse = query[0]

    query = list(MyUser.objects.filter(username__iexact=data["taUsername"]))
    if len(query) == 0:
        return ErrorString("Error: user does not exist")

    if query[0].position != str(UserType.TA):
        return ErrorString("Error: user is not a TA")

    tempUser = query[0]

    if TAsToCourses.objects.filter(TA=tempUser, course=tempCourse).exists():
        return ErrorString("Error: TA has already been assigned to course")

    TAsToCourses.objects.create(TA=tempUser, course=tempCourse)

    return True


def assign_instructor(data: dict, all=False) -> Union[ErrorString, bool]:
    """handles assigning an instructor to a course section in the given data. On failure returns ErrorString describing error.
    On success, returns True. Warning: will override an existing instructor of a course
    if all is given as True, then the instructor will be assigned to all courses"""
    needed = [("designation", str), ("instructorUsername", str)]
    if not all:
        needed.append(("courseSection", int))
    check = verify_dict(needed, data)
    if not check:
        return check

    query = CourseSections.objects.filter(course__designation__iexact=data["designation"])
    if not all:
        query = query.filter(section=data["courseSection"])
    query = list(query)
    if not query:
        return ErrorString("Error: course/sections not found")

    tempSections = query

    query = list(MyUser.objects.filter(username__iexact=data["instructorUsername"]))
    if not query:
        return ErrorString("Error: user not found")

    tempUser = query[0]

    if tempUser.position is not str(UserType.INSTRUCTOR):
        return ErrorString("Error: user is not an instructor")

    if all:
        for section in tempSections:
            section.instructor = tempUser
            section.save()
    else:
        tempSections[0].instructor = tempUser
        tempSections[0].save()

    return True


def get_userdata(username: str) -> Union[ErrorString, dict]:
    """gets the userdata of a certain user"""
    if type(username) is not str:
        return ErrorString("Error: wrong type for username")

    temp = MyUser.objects.filter(username__iexact=username)
    if not temp:
        return ErrorString("Error: user not found")

    temp = temp[0]

    return {"username": username, "first_name": temp.first_name, "last_name": temp.last_name, "addressln1": temp.addressln1,
            "addressln2": temp.addressln2, "email": temp.email, "phone_number": temp.phone_number}


def get_sections_of_instructor(data: dict) -> list:
    needed = [("username", str), ("designation", str)]
    check = verify_dict(needed, data)
    if not check:
        return check

    sections = CourseSections.objects.filter(instructor__username__iexact=data['username'], course__designation__iexact=data['designation'])

    return list(sections)


def get_course_id_by_name(courseName: str) -> Union[ErrorString, int]:
    """gets the id of a course by its name (case insensitive). Returns the id on success, or an ErrorString saying
    whether the course did not exist or if data were invalid"""
    if type(courseName) is not str:
        return ErrorString("Error: incorrect data")

    if not CourseData.objects.filter(title__iexact=courseName).exists():
        return ErrorString("Error: course does not exist")

    return CourseData.objects.get(title__iexact=courseName).id


def list_courses() -> Union[ErrorString, dict]:
    """gets a list of all the courses: a triple of 1 course string, 2 list of associated sections, 3 list of associated labs"""
    #result = []
    courses = CourseData.objects.all()
    #for c in courses:
    #   result.append((str(c), list(map(str, CourseSections.objects.filter(course=c))), list(map(str, LabData.objects.filter(course=c)))))
    for c in courses:
        yield (str(c), c.designation, list(map(str, CourseSections.objects.filter(course=c))),
                       list(map(str, LabData.objects.filter(course=c))))


def list_users() -> list:
    """gets a list of all the users in the database as a list of triples containing the name of the user, their position, and their username"""
    users = []
    for i in MyUser.objects.all():
        users.append((str(i), i.position, i.username))
    return users


def list_instructors() -> list:
    for i in MyUser.objects.all():
        if i.position == "I":
            yield (str(i), i.username)


def list_tas() -> list:
    for i in MyUser.objects.all():
        if i.position == "T":
            yield (str(i), i.username)


def get_userdata(username: str) -> Union[ErrorString, dict]:
    """gets the userdata of a certain user"""
    if type(username) is not str:
        return ErrorString("Error: wrong type for username")

    temp = MyUser.objects.filter(username__iexact=username)
    if not temp:
        return ErrorString("Error: user not found")

    temp = temp[0]

    return {"username": username, "first_name": temp.first_name, "last_name": temp.last_name, "addressln1": temp.addressln1,
            "addressln2": temp.addressln2, "email": temp.email, "phone_number": temp.phone_number}


def get_coursedata(designation: str) -> Union[ErrorString, dict]:
    if type(designation) != str:
        return ErrorString("Error: wrong type for designation")
    temp = list(CourseData.objects.filter(designation__iexact=designation))
    if not temp:
        return ErrorString("Error: course does not exist")
    temp = temp[0]
    return {"designation": designation,
            "title": temp.title,
            "sections": list(CourseSections.objects.filter(course=temp)),
            "labs": list(LabData.objects.filter(course=temp)),
            "semester": temp.semester}


def get_tas_of_course(designation: str) -> Union[ErrorString, list]:
    if type(designation) != str:
        return ErrorString("Error: wrong type for designation")
    tempcourse = list(CourseData.objects.filter(designation__iexact=designation))
    if not tempcourse:
        return ErrorString("Error: no course with given designation found")
    tempcourse = tempcourse[0]
    for i in TAsToCourses.objects.filter(course=tempcourse):
        yield (str(i.TA), i.TA.username)


def update_ta_skill(data: dict):
    needed = [("taUsername", str), ("skills", str)]
    check = verify_dict(needed, data)
    if not check:
        return check

    tempuser = MyUser.objects.filter(username__iexact=data["taUsername"])
    if not tempuser.exists():
        return ErrorString("Error: user not found")

    tempuser = tempuser[0]

    if tempuser.position != "T":
        return ErrorString("Error: user is not TA")

    print(tempuser)

    TASkills.objects.update_or_create(TA=tempuser, defaults={"skills": data["skills"]})

    return True


def get_skills(taUsername: str):
    if type(taUsername) != str:
        return ErrorString("Error: taUsername is not str")

    tempuser = list(MyUser.objects.filter(username__iexact=taUsername))

    if not tempuser:
        return ErrorString("Error: user not found")

    tempuser = tempuser[0]

    if tempuser.position != "T":
        return ErrorString("Error: user is not TA")

    skills = list(TASkills.objects.filter(TA=tempuser))

    if not skills:
        return ""

    return skills[0].skills


def get_courses_of_instructor(instructorUsername: str):
    if type(instructorUsername) != str:
        return ErrorString("Error: wrong type for instructorUsername")

    tempinstructor = list(MyUser.objects.filter(username=instructorUsername))
    if not tempinstructor:
        return ErrorString("Error: instructor not found")

    tempinstructor = tempinstructor[0]

    if tempinstructor.position != "I":
        return ErrorString("Error: user is not instructor")

    courses = CourseData.objects.filter(coursesections__instructor=tempinstructor).distinct()

    return list(courses)


def delete_account(username: str) -> Union[ErrorString, bool]:
    if type(username) != str:
        return ErrorString("Error: wrong type for username")

    tempuser = list(MyUser.objects.filter(username__iexact=username))

    if not tempuser:
        return ErrorString("Error: user not found")

    tempuser[0].delete()

    return True


def get_all_user_info(isSupervisor=False):
    def allInfo(user: MyUser):
        return (user.username, user.position, user.get_full_name(), user.email, user.phone_number, user.addressln1, user.addressln2)

    def publicInfo(user: MyUser):
        return (user.username, user.position, user.get_full_name(), user.email)

    users = MyUser.objects.all()

    func = allInfo if isSupervisor else publicInfo

    for i in users:
        yield func(i)
