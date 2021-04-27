from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import MyUser, UserType, CourseData, CourseSections, LabData, TAsToCourses
admin.site.register(MyUser)
admin.site.register(CourseData)
admin.site.register(CourseSections)
admin.site.register(LabData)
admin.site.register(TAsToCourses)