from django.urls import path, include

from .views import *

urlpatterns = [
    path('parse_grades/', parse_grades),
    path('students_rating/', students_rating),
    path('schools_rating/', schools_rating),
    path('', write_db),
]