from django.urls import path
from examate import views
from .views import *
from django.urls import path

urlpatterns = [
    path('about',views.about),
    path('register',views.register),
    path('login',views.login),
    path('',views.index),
    path('header',views.header),
    path('footer',views.footer),
    path('contact',views.contact),
    path('cexam',views.createexam),
    path('logout',views.user_logout),
    path('edit/<rid>',views.edit),
    path('sedit/<rid>',views.sedit),
    path('que/<rid>',views.addque),
    path('delete/<rid>',views.delete),
    path('sdelete/<rid>',views.sdelete),
    path('udash',views.dashboard),
    path('logout',views.user_logout),
    path('token',views.token_send),
    path('mail',views.mail_vari),
    path('verify/<auth_token>',views.verify),
    path('error',views.error), 
    path('addstudent',views.addstudent), 
    path('studentdash',views.studentdash), 
    path('submitexam/<auth_token>/<rid>',views.subexam), 
    path('userreg',views.user_reg),
    path('userlogin',views.userlogin),
]



'''
syntax:
path('pattern',views.functionname,name)
'''