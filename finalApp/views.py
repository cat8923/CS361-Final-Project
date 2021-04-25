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

class EditLab(View):
    def get(self, request):
        return render(request, "createLab")

    def post(self, request):
        NoSuchUser = False
        badPassword = False
        try:
            # check to see if there is a user with the chosen name
            # create a variable with that person's details
            # redirect to create lab and save all information
        except:
            noSuchUser=True

        if noSuchUser:
            return render(request, "createLab", {"message":"Username not recognized."})
        elif badPassword:
            return render(request, "createLab", {"message":"Password incorrect"})
        else:
            request.session["username"] = MyUser.username
            return redirect("createLab")
