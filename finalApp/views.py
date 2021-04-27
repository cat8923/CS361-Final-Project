from django.shortcuts import render
from django.views import View
from finalApp import database_access


class CreateCourse(View):
    def get(self,request):
        if len(request.GET) == 0:
            TA = list(filter(lambda x: x[1] == 'T', database_access.list_users()))
            return render(request, "create_course.html", {"TA": TA})

    def post(self,request):
        courseDict = {
            "title": request.GET["description"],
            "section": request.GET["designation"],
        }
        database_access.make_course(courseDict)


class CourseList(View):
    def get(self, request):
        if len(request.GET) == 0:
            courses = list(database_access.list_courses())
            return render(request, "course_list.html", {"courses": courses})




