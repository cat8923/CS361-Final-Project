from django.shortcuts import render, redirect
from django.views import View

# Create your views here.

class Login(View):
    def get(self, request):
        return render(request, "Login.html")

    def post(self, request):
        NoSuchUser = False
        badPassword = False
        try:
            # check to see if there is a user with the chosen name

        except:
            noSuchUser=True

        if noSuchUser:
            return render(request, "Login.html", {"message":"Username not recognized."})
        elif badPassword:
            return render(request, "Login.html", {"message":"Password incorrect"})
        else:
            request.session["username"] = user.username
            return redirect("/Homepage/")




class Homepage(View):
    def get(self, request):
        return render(request, "Homepage.html")

    def post(self, request):
        click = request.POST['onclick']
        if click == 'accounts':
            return redirect("/accounts/")
        elif click == 'courses':
            return redirect("/courses/")
        elif click == 'logout':
            return render(request, "Login.html")