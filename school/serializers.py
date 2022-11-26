from email.message import EmailMessage
from rest_framework.serializers import ModelSerializer, CharField, Serializer, URLField
from django.forms import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model


# from .models import Student, Director
from documents.models import Counselor

# from account.models import ResetPassword

User = get_user_model()


class StudentRegisterSerializer(ModelSerializer):
    inn = CharField(required=True, write_only=True, min_length=True)
    password = CharField(min_length=6, required=True, write_only=True)
    
    
    class Meta:
        model = User
        fields = ('email', 'password', 'inn')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('Student with this email already exists')
        return value


    def validate_inn(self, value):
        if not str(value).isdigit():
            raise ValidationError('INN must be number')
        if not str(value).startswith('1'):
            raise ValidationError('INN must start with 1 or 2')
        return value


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# or not str(value).startswith('2')
    # def school_name(self):
    #     inn = self.validate_inn()
    #     school_name = Counselor.objects.get(inn)
    #     print("SCHOOL_NAME=>", school_name['school_name'])
    #     return school_name['school_name']


    # def create(self, validated_data):
    #     print("VALIDATED_DATA=>", validated_data)
    #     # user = User.objects.create_user(**validated_data)
    #     user = super().save(commit=False)
    #     user.is_student = True
    #     user.activate()
    #     user.save()
    #     student = Student.objects.create(user = user)
    #     student.create_activation_code()
    #     inn = self.validate_inn()
    #     school_name = Counselor.objects.get(inn)
    #     print("SCHOOL_NAME=>", school_name['school_name'])
    #     student.inn.add(inn)
    #     student.school.add(school_name['school_name'])
    #     return user


        # return Student.objects.create_user(**validated_data)



# class DirectorRegisterSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_director = True
#         if commit:
#             user.save()
#         return user



class LoginSerializer(TokenObtainPairSerializer):
    pass