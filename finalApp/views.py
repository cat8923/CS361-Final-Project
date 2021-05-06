from django.shortcuts import render, redirect
from django.views import View
from finalApp.database_access import login, ErrorString
from finalApp import database_access
from .models import CourseData
# Create your views here.

class Login(View):
    def get(self, request):
        return render(request, "Login.html", {})

    def post(self, request):
        user = login({"username": request.POST["username"], "password": request.POST["password"]})

        if not user:
            return render(request, "Login.html", {"message": str(user)})
        else:
            request.session["first_name"] = user["first_name"]
            request.session.save()
            return redirect("/Homepage/")


class Homepage(View):
    def get(self, request):
        name = request.session['first_name']
        return render(request, "Homepage.html", {'name': name})

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
            return render(request, "create_course.html", {"TA": TA})

    def post(self, request):

        courseDict = {
            "title": request.POST["description"],
            #"section": request.POST["designation"],
        }
        database_access.make_course(courseDict)

        click = request.POST['onclick']
        if click == 'Logout':
            request.session.flush()
            return render(request, "Login.html")

        
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
            courses = list(CourseData.objects.all())
            return render(request, "course_list.html", {"courses": courses})

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
        course = self.kwargs
        return render(request, "edit_course.html", course)

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
