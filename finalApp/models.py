from django.db import models as m
from django.contrib.auth import models
# Create your models here.


class UserType(m.TextChoices):
    SUPERVISOR = "S"
    INSTRUCTOR = "I"
    TA = "T"


class MyUser(models.User):
    position = m.CharField(max_length = 1, choices = UserType.choices, default = UserType.TA)

    def __str__(self):
        return self.get_full_name()