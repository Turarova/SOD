from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('register/student/', StudentRegisterView.as_view()),
    path('register/director/', DirectorRegisterView.as_view()),
    path('login/student/', LoginStudentView.as_view()),
    path('login/director/', LoginDirectorView.as_view()),
    path('activation/', ActivationView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
]