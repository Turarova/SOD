from rest_framework import serializers
from .models import *


class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocument
        exclude = ('quarters_1_grade', 'quarters_2_grade', 'quarters_3_grade', 'quarters_4_grade', 'years_grade', 'subject', 'counselors_inn', 'users_inn')

    def get(self):
        print(self)