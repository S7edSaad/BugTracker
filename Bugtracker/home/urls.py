# Copyright © 2024 Syed Saad Ali
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.loginuser, name='Login'),
    path("home", views.index, name='Home'),
    path("login",views.loginuser,name='login'),
    path("logout",views.logoutuser,name='logout'),
    path("register",views.register,name='register'),
    path('staff',views.staff,name='Staff'),
    path('project',views.project,name='Project'),
    path('createproject',views.createproject,name='Createproject'),
    path('addproject',views.addproject,name='Addproject'),
    path('editproject/<int:id>',views.editproject,name='Editproject'),
    path('updateproject/<int:id>',views.updateproject,name='Updateproject'),
    path('Userproject',views.Userproject,name='Project'),
    path('displayusers',views.displayusers,name='Users'),    
    path('staffdisplayusers',views.staffdisplayusers,name='Users'),
    path('deleteproject/<int:id>',views.deleteproject,name='Deleteproject'),
    path('addbug',views.addbug,name='Add Bug'),
    path('bugs',views.bugs,name='Bugs'),
    path('editbug/<int:id>',views.editbug,name='Edit bug'),
    path('deletebug/<int:id>',views.deletebug,name='Delete bug'),
    path('tasks/<str:username>',views.displaytasks,name='Display task'),
    path('clientbugs',views.displayclientbugs,name='Bugs'),
    path('base',views.base,name='Home'),
    path('back',views.back,name='Home'),
    path('viewproject/<int:id>',views.viewproject,name='View Project'),
    path('projectbugbar',views.project_bug_graph,name='Bar graph'),
    path('reportdate',views.reportdate,name='Report Date'),
    path('editaccount',views.editaccount,name='Edit Account'),
    path('reportusers',views.reportusers,name='User Report'),
    path('admindisplayusers',views.staffdisplayusers,name='Admin users'),
    path('adduser',views.adduser,name='Admin add users'),
    path('deleteuser/<str:username>',views.deleteuser,name='Delete User'),
    path('edituser/<str:username>',views.edituser,name='Edit User'),
]