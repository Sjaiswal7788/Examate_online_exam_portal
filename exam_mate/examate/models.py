from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):

    stitle=models.CharField(max_length=50)
    que=models.CharField(max_length=500)
    date=models.DateField(default=datetime.date(1900,1,1))
    time=models.TimeField(default=datetime.time(00,00,00))
    year=models.IntegerField()
    uid=models.IntegerField()
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at =  models.DateTimeField(auto_now_add=True)

    

class que(models.Model):

    que=models.CharField(max_length=500)
    uid=models.IntegerField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at =  models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class student(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    year = models.IntegerField()


# class subexam(models.Model):
#     name=models.CharField(max_length=100)
#     answer=models.CharField(max_length=1000)