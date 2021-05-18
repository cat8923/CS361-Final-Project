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
from finalApp.views import Login, Homepage, CreateCourse, CourseList, CreateAccount, Blank, Logout, TestCreate, EditAccount, AccountList, EditCourse
import finalApp.views as fav

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Blank.as_view()),
    path('Account_List/', AccountList.as_view(), name='accountlist'),
    path('edit_account/', EditAccount.as_view()),
    path('Logout/', Logout.as_view(), name='logout'),
    path('Login/', Login.as_view()),
    path('Homepage/', Homepage.as_view(), name='home'),
    path('Create_Course/', CreateCourse.as_view(), name='createcourse'),
    path('Course_List/', CourseList.as_view(), name="courses"),
    path('create_account/', CreateAccount.as_view(), name='createaccount'),
    path('test_create/', TestCreate.as_view(), name="test"),
    path('edit_self/', fav.EditSelf.as_view(), name='editself'),
    url(r'^account_list/(?P<account>[a-zA-Z0-9]+)', fav.AccountList.as_view(), name='accountlist'),
    url(r'^my_courses/(?P<course>[a-zA-Z0-9]+)/(?P<lab>[0-9]+)', fav.MyCourses.as_view(), name='mycourses'),
    url(r'^my_courses/(?P<course>[a-zA-Z0-9]+)', fav.MyCourses.as_view(), name='mycourses'),
    url('Edit_Account/(?P<username>[a-zA-Z0-9]+)', EditAccount.as_view(), name='edit'),
    url(r'^my_courses/', fav.MyCourses.as_view(), name='mycourses'),
    url(r'^test_create/(?P<username>[a-zA-Z0-9]+)', TestCreate.as_view(), name="test"),
    url(r'^Edit_Course/(?P<course>[a-zA-Z0-9]+)/addsection/', fav.AddSection.as_view(), name='addsection'),
    url(r'^Edit_Course/(?P<course>[a-zA-Z0-9]+)/assigntatocourse/', fav.AssignTasToCourse.as_view(), name='assigntas'),
    url(r'^Edit_Course/(?P<course>[a-zA-Z0-9]+)/assigninstructor/(?P<section>[0-9]+)', fav.AssignInstructor.as_view(), name='addinst'),
    url(r'^Edit_Course/(?P<course>[a-zA-Z0-9]+)/addtatolab/(?P<lab>[0-9]+)', fav.AssignTasToLab.as_view(), name='addta'),
    url(r'^Edit_Course/(?P<course>[a-zA-Z0-9]+)/add', EditCourse.as_view(), name='edit'),
    url(r'^Edit_Course/(?P<course>[a-zA-Z0-9]+)', EditCourse.as_view(), name='edit'),
    url(r'.*', Blank.as_view())
]
