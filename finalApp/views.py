from django.shortcuts import render,redirect
from django.views import View
from finalApp import database_access

# Create your views here.

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



