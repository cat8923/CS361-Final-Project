from django.shortcuts import render, redirect
from django.views import View
from Final_Project.models import MyUser

# Create your views here.

class AddLab(View):
    def get(self, request):
        return render(request, "createLab")

    def post(self, request):
        noSuchUser = False
        badPassword = False

        if noSuchUser:
            return render(request, "createLab", {"message":"Username not recognized."})
        elif badPassword:
            return render(request, "createLab", {"message":"Password incorrect"})
        else:
            request.session["username"] = MyUser.username
            return redirect("createLab")


