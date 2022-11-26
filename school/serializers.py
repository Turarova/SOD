from email.message import EmailMessage
from rest_framework.serializers import ModelSerializer, CharField, Serializer, URLField
from django.forms import ValidationError

from .models import Student
from documents.models import Counselor

# from account.models import ResetPassword



class RegisterSerializer(ModelSerializer):
    inn = CharField(required=True, write_only=True, min_length=True)
    password = CharField(min_length=6, required=True, write_only=True)
    
    
    class Meta:
        model = Student
        fields = ('inn', 'email', 'password')

    def validate_email(self, value):
        if Student.objects.filter(email=value).exists():
            raise ValidationError('Student with this email already exists')
        return value


    def validate_inn(self, value):
        if not str(value).isdigit():
            raise ValidationError('INN must be number')
        if not str(value).startswith('1') or not str(value).startswith('2'):
            raise ValidationError('INN must start with 1 or 2')
        return value


    def school_name(self):
        inn = self.validate_inn()
        school_name = Counselor.objects.get(inn)
        print("SCHOOL_NAME=>", school_name['school_name'])
        return school_name['school_name']


    def create(self, validated_data):
        Student.is_active()
        print("VALIDATED_DATA=>", validated_data)
        # return Student.objects.create_user(**validated_data)