from django.urls import path, include

from .views import parse_grades

urlpatterns = [
    path('test/', parse_grades),
]