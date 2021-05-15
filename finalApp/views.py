from django.shortcuts import render, redirect
from django.views import View
from finalApp.database_access import login, ErrorString
from finalApp import database_access
from .models import CourseData, MyUser, UserType
# Create your views here.


class EditSelf(View):
    def get(self, request):
        return render(request, "edit_self.html", {"user": database_access.get_userdata(request.session['username']),
                                                  "position": request.session['position'],
                                                  "username": request.session['username']})

    def post(self, request):
        check = database_access.update_user(request.POST)
        return render(request, "edit_self.html", {"user": database_access.get_userdata(request.session['username']),
                                                  "position": request.session['position'], "message": str(check) if not check else "Success!"})


class AddSection(View):
    def get(self, request, **kwargs):
        pass


class AssignTas(View):
    pass


class AssignInstructor(View):
    def get(self, request, **kwargs):
        return render(request, "assign_instructor.html", {"pagetitle": "Assign Instructor",
                                                          "designation": self.kwargs.get("course"),
                                                          "section": self.kwargs.get("section"),
                                                          "instructors": database_access.list_instructors()})

    def post(self, request, **kwargs):
        check = database_access.assign_instructor({"instructorUsername": request.POST["instructorUsername"],
                                                   "designation": self.kwargs.get("course"),
                                                   "courseSection": int(self.kwargs.get("section"))})
        return render(request, "assign_instructor.html", {"pagetitle": "Assign Instructor",
                                                          "designation": self.kwargs.get("course"),
                                                          "section": self.kwargs.get("section"),
                                                          "instructors": database_access.list_instructors(),
                                                          "message": str(check) if not check else "Success"})


class TestCreate(View):
    def get(self, request, **kwargs):
        li = database_access.list_courses()
        return render(request, "create_test_user.html", {"list": li, "username": self.kwargs.get("username"), "users": database_access.list_users()
                                                         , "courses": database_access.get_coursedata("cs351")})

    def post(self, request):
        check = database_access.make_user(request.POST)
        if not check:
            return render(request, "create_test_user.html", {"message": str(check)})
        else:
            return render(request, "create_test_user.html", {"message": "success"})


class Blank(View):
    def get(self, request):
        if request.session.get("first_name"):
            return redirect("/Homepage/")
        else:
            return redirect("/Login/")


class Logout(View):
    def get(self, request):
        request.session.flush()
        return redirect("/Login/")


class Login(View):
    def get(self, request):
        return render(request, "Login.html")

    def post(self, request):
        user = login({"username": request.POST["username"], "password": request.POST["password"]})

        if not user:
            return render(request, "Login.html", {"message": str(user)})
        else:
            request.session["first_name"] = user["first_name"]
            request.session["position"] = user["position"]
            request.session["username"] = request.POST['username']
            request.session.save()
            return redirect("/Homepage/")


class Homepage(View):
    def get(self, request):

        name = request.session.get('first_name')
        if name:
            return render(request, "Homepage.html", {'name': name, 'pagetitle': "Homepage"})
        else:
            return redirect("/Login/")

    def post(self, request):
        click = request.POST['onclick']
        if click == 'Accounts':
            return redirect("/Account_List/")
        elif click == 'Courses':
            return redirect("/Course_List/")
        elif click == 'Logout':
            request.session.flush()
            return render(request, "Login.html")


class CreateCourse(View):
    def get(self, request):
        if len(request.GET) == 0:
            TA = list(filter(lambda x: x[1] == 'T', database_access.list_users()))
            return render(request, "create_course.html", {"TA": TA, "pagetitle": "Create Course"})

    def post(self, request):
        check = database_access.make_course({"title": request.POST['title'], "designation": request.POST['designation'],
                                             "section": int(request.POST['section']), "semester": request.POST['semester']})
        return render(request, "create_course.html", {"message": str(type(request.POST['section'])) if not check else "success"})

        
class AddLab(View):
        def get(self, request):
            if len(request.GET) == 0:
                TA = list(filter(lambda x: x[1] == 'T', database_access.list_users()))
                return render(request, "/Create_Lab/", {"TA": TA})

        def post(self, request):
            labDict = {
                "courseID": request.GET["description"],
                "section": request.GET["designation"],
            }
            database_access.make_lab(labDict)


class CourseList(View):
    def get(self, request):
        if len(request.GET) == 0:
            #courses = list(database_access.list_courses())
            courses = database_access.list_courses()
            return render(request, "course_list.html", {"courses": courses, "pagetitle": "List of Courses"})

    def post(self, request):
        click = request.POST['onclick']
        if click == 'Create New Course':
            return redirect("/Create_Course/")
        elif click == 'Edit Course':
            print(request.POST)
            course = request.POST['courses']
            return redirect("/Edit_Course/"+course+"/")
        elif click == 'Logout':
            request.session.flush()
            return render(request, "Login.html")


class AccountView(View):
    def get(self, request):
        if len(request.GET) == 0:
            accounts = list(database_access.list_users())
            return render(request, "account_list.html", {"accounts": accounts})

          
class CreateAccount(View):
    def get(self, request):
        return render(request, "create_account.html")

    def post(self, request):
        '''
        accountDict = {
            "username": request.POST["description"],
            "password": request.POST["description"],
            "first_name": request.POST["description"],
            "last_name": request.POST["description"],
            "address": request.POST["description"],
            "title": request.POST["description"],
            "email": request.POST["description"],
            "number": request.POST["description"],
        }
        '''
        message = database_access.make_user(request.POST)
        if message:
            message = "successfully created account"
        else:
            message = str(message)

        return render(request, "Homepage.html", {"message": message})

class EditCourse(View):
    def get(self, request, **kwargs):
        print(self.kwargs)
        course = self.kwargs.get("course")
        if course:
            course = database_access.get_coursedata(course)
            #instructors = database_access.get_instructors()
            instructors = list(MyUser.objects.filter(position=str(UserType.INSTRUCTOR)))
            TAs = list(MyUser.objects.filter(position=str(UserType.TA)))
        else:
            course = {}
        data = {"course": course, "instructors": instructors, "TA": TAs, "pagetitle": "Edit Course"}
        print(data)

        return render(request, "edit_course.html", data)

    def post(self, request):
        click = request.POST['onclick']
        if click == 'Logout':
            request.session.flush()
            return redirect('')
        elif click == 'Save Edit':
            # need to save the changes we made first
            course = self.kwargs
            return render(request, "edit_course.html", course)
        elif click == 'Cancel Edit':
            course = self.kwargs
            return render(request, "edit_course.html", course)
        elif click == 'Delete Course':
            return redirect('/course_list/')
        elif click == 'Create New Course':
            return redirect('/create_course/')
        elif click == 'Add Section':
            pass
        elif click == 'Add Lab':
            pass
