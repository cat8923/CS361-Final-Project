from django.shortcuts import render, redirect
from django.views import View
from finalApp.database_access import login, ErrorString

# Create your views here.

class Login(View):
    def get(self, request):
        return render(request, "Login.html")

    def post(self, request):
        user = login({request.POST(name="username"), request.POST(password="password")})

        if not user:
            return render("Login.html", message=str(user))
        else:
            request.session["username"] = user.username
            return redirect("/Homepage/")




class Homepage(View):
    def get(self, request):
        name = request.session['first_name']
        return render(request, "Homepage.html", {'name': name})

    def post(self, request):
        click = request.POST['onclick']
        if click == 'accounts':
            return redirect("/account_list/")
        elif click == 'courses':
            return redirect("/course_list/")
        elif click == 'logout':
            return render(request, "Login.html")