"""finalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from finalApp.views import Login, Homepage, AddLab, CreateCourse, CourseList, CreateAccount, Blank, Logout, TestCreate, \
    EditAccount, AccountList  # EditLab,

from finalApp.views import Login, Homepage, AddLab, CreateCourse, CourseList, CreateAccount, Blank, Logout, TestCreate, EditCourse, AssignTas #EditLab
import finalApp.views as fav

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Blank.as_view()),
    path('Logout/', Logout.as_view(), name='logout'),
    path('Login/', Login.as_view()),
    path('Homepage/', Homepage.as_view(), name='home'),
    path('createLab/', AddLab.as_view()),
    path('Create_Course/', CreateCourse.as_view(), name='createcourse'),
    path('Course_List/', CourseList.as_view(), name="courses"),
    path('create_account/', CreateAccount.as_view()),
    path('test_create/', TestCreate.as_view()),
    path('Account_List/', AccountList.as_view()),
    path('edit_account/', EditAccount.as_view()),
    url(r'^edit_account/(?P<username>[a-zA-Z0-9]+)', TestCreate.as_view(), name="test"),
    url('Edit_Account/(?P<username>[a-zA-Z0-9]+)', EditAccount.as_view(), name='edit')

]
