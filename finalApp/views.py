from django.shortcuts import render, redirect, user
from django.views import View

# Create your views here.

class LabScreen(View):
    def get(self, request):
        return render(request, "create_Lab.html")

    def post(self, request):
        NoSuchUser = False
        badPassword = False
        try:
            # check to see if there is a user with the chosen name

        except:
            noSuchUser=True

        if noSuchUser:
            return render(request, "create_Lab.html", {"message":"Username not recognized."})
        elif badPassword:
            return render(request, "create_Lab.html", {"message":"Password incorrect"})
        else:
            request.session["username"] = user.username
            return redirect("/create_Lab/")




class Homepage(View):
    def get(self, request):
        return render(request, "create_Lab.html")

    def post(self, request):
        click = request.POST['onclick']
        if click == 'edit':
            return redirect("/editLab/")
        elif click == 'Logout':
            return redirect("/Login/")
        elif click == 'logout':

