from django.urls import path
from .views import *

urlpatterns = [
    path('', write_db),
    path('test/', parse_grades),
]