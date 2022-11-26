from rest_framework import serializers
from .models import *


class Counselor(serializers.ModelSerializer):
    class Meta:
        model = StudentDocument
        exclude = ('grade', 'subject', 'counselors_inn', 'users_inn')