from django.db import models as m
from django.contrib.auth import models


# Create your models here.


class UserType(m.TextChoices):
    SUPERVISOR = "S"
    INSTRUCTOR = "I"
    TA = "T"


class MyUser(models.User):
    position = m.CharField(max_length=1, choices=UserType.choices, default=UserType.TA, null=False)
    addressln1 = m.CharField(max_length=50, null=True)
    addressln2 = m.CharField(max_length=50, null=True)
    phone_number = m.CharField(max_length=12, null=True)

    def __str__(self):
        return self.get_full_name()


class CourseData(m.Model):
    title = m.CharField(max_length=50, unique=True)
    designation = m.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.title + " - " + self.designation


class CourseSections(m.Model):
    course = m.ForeignKey(CourseData, on_delete=m.CASCADE, null=False)
    section = m.IntegerField(null=False)
    instructor = m.ForeignKey(MyUser, on_delete=m.SET_NULL, null=True)

    def __str__(self):
        return str(self.course) + " " + str(self.section)

    def __repr__(self):
        return self.course.designation + " " + str(self.section)


class LabData(m.Model):
    course = m.ForeignKey(CourseData, on_delete=m.CASCADE, null=False)
    TA = m.ForeignKey(MyUser, on_delete=m.SET_NULL, null=True)
    section = m.IntegerField(null=False)

    def __str__(self):
        return str(self.section) + (("TA: " + self.TA.get_full_name() + " ") if self.TA else "")


class TAsToCourses(m.Model):
    TA = m.ForeignKey(MyUser, on_delete=m.CASCADE, null=False)
    course = m.ForeignKey(CourseData, on_delete=m.CASCADE, null=False)
    skills = m.TextField()
