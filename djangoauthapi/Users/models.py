from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import CustomUserManager
# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    cnic = models.CharField(max_length=13)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','cnic','city']

    objects = CustomUserManager()

    # def __str__(self):
    #     return self.name
