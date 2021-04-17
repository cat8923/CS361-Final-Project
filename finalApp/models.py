from django.db import models as m
from django.contrib.auth import models


# Create your models here.


class UserType(m.TextChoices):
    SUPERVISOR = "S"
    INSTRUCTOR = "I"
    TA = "T"


class MyUser(models.User):
    position = m.CharField(max_length=1, choices=UserType.choices, default=UserType.TA, null=False)
    address = m.CharField(max_length=50, null=True)
    phone_number = m.CharField(max_length=12, null=True)

    def __str__(self):
        return self.get_full_name()


class CourseData(m.Model):
    title = m.CharField(max_length=20)
    instructor = m.ForeignKey(MyUser, on_delete=m.SET_NULL, null=True)


class LabData(m.Model):
    course = m.ForeignKey(CourseData, on_delete=m.CASCADE, null=False)
    TA = m.ForeignKey(MyUser, on_delete=m.SET_NULL, null=True)


class TAsToCourses(m.Model):
    TA = m.ForeignKey(MyUser, on_delete=m.CASCADE, null=False)
    course = m.ForeignKey(CourseData, on_delete=m.CASCADE, null=False)
