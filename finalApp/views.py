from django.shortcuts import render, redirect
from django.views import View
from finalApp.database_access import login, ErrorString
from finalApp import databse_access


# Create your views here.
class AccountView(View):
    def get(self, request):
        if len(request.GET) == 0:
            accounts = list(database_access.list_users())
            return render(request, "account_list.html", {"accounts": accounts})

class CreateAccount(View):
    def get(self, request):
        pass

    def post(self, request):
        accountDict = {
            "username": request.GET["description"],
            "password": request.GET["description"],
            "first_name": request.GET["description"],
            "last_name": request.GET["description"],
            "address": request.GET["description"],
            "title": request.GET["description"],
            "email": request.GET["description"],
            "number": request.GET["description"],
        }
        database_access.make_user(accountDict)
