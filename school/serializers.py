from email.message import EmailMessage
from rest_framework.serializers import ModelSerializer, CharField, Serializer, URLField
from django.forms import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .tasks import send_pass_res
from .models import PasswordReset


import random
import string

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
        if not str(value).startswith('1') and not str(value).startswith('2'):
            raise ValidationError('INN must start with 1 or 2')
        return value


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class DirectorRegisterSerializer(ModelSerializer):
    password = CharField(min_length=6, required=True, write_only=True)
    
    
    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('Director with this email already exists')
        return value
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        


class ActivationSerializer(Serializer):
    activation_code = CharField(required=True, write_only=True, max_length=255)


class LoginStudentSerializer(TokenObtainPairSerializer):
    inn = CharField(required=True, write_only=True, min_length=True)

    class Meta:
        model = User
        fields = '__all__' 


class LoginDirectorSerializer(TokenObtainPairSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def validate_email(self, value):
        if User.objects.get(email=value).is_student != False:
            raise ValidationError('Director with this email doesn\'t exists')


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True,
                                         min_length=8, write_only=True)


class PasswordResetEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PasswordReset
        fields = '__all__'

    def validate(self, attrs):
        try:
            email = attrs.get('email')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                new_password = ''.join((random.choice(string.ascii_lowercase + string.digits)) for x in range(8))
                send_pass_res.delay(user.email, new_password)
                user.password = new_password
                user.set_password(new_password)
                user.save()
            return attrs
        except Exception as e:
            raise ValidationError()