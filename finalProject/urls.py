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

from finalApp.views import Login, Homepage, AddLab, CreateCourse, CourseList #EditLab


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view()),

    path('Homepage/', Homepage.as_view()),
    path('createLab/',AddLab.as_view()),
    #path('editLab/',EditLab.as_view())
    path('Create_Course/',CreateCourse.as_view()),

    #path('/Edit_Course/' , EditCourse.as_view()),
    path('Course_List/' , CourseList.as_view())
]
