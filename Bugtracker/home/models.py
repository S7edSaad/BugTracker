# Copyright © 2024 Syed Saad Ali
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Createuser(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    passw = models.CharField(max_length=50)


class Project(models.Model):
    Pname = models.CharField(max_length=122)
    Pstatus = models.CharField(max_length=122)
    Desc = models.TextField()
    date = models.DateField()
    def __str__(self):
        return self.Pname

class Bug(models.Model):
    project = models.CharField(max_length=122,null=True)
    Severity = models.CharField(max_length=122,null=True)
    Priority = models.CharField(max_length=122,null=True)
    Assign = models.CharField(max_length=122,null=True)
    Summary = models.TextField(null=True)
    Desc = models.TextField(null=True)
    date = models.DateField()
    Image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    status = models.CharField(max_length=50,default='Unresolved')
    created = models.DateTimeField(auto_now_add = True)
    ended = models.DateField(null=True,blank=True)
    timetaken = models.CharField(max_length=50,null=True,blank=True)
    reportedby = models.CharField(max_length=50)
    resolvedby = models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return self.project