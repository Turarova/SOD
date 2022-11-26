from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import *


class Counselor(serializers.ModelSerializer):
    class Meta:
        model = StudentDocument
        exclude = ('grade', 'subject', 'counselors_inn', 'users_inn')

        