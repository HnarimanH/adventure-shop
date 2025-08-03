from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    profilePic = models.IntegerField(null=True, blank=True)