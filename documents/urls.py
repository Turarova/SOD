from django.urls import path, include

from .views import parse_grades, schools_rating, students_rating

urlpatterns = [
    path('parse_grades/', parse_grades),
    path('students_rating/', students_rating),
    path('schools_rating/', schools_rating),
]