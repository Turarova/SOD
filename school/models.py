from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=255)



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)


        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)




class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField('email address', unique=True)
    password = models.CharField(max_length=100)
    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    



class Director(User):
    pass
    


class Student(User):
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name='school')
    inn = models.CharField(max_length=15, unique=True) 
    activation_code = models.CharField(max_length=36, blank=True)
    is_student = models.BooleanField(default=True)


    def activate_with_code(self, code):
        if str(self.activation_code) != str(code):
            raise Exception(('code does not match'))
        self.is_active = True
        self.activation_code = ''
        self.save(update_fields=['is_active', 'activation_code'])

    def create_activation_code(self):
        code = str(uuid.uuid4())
        self.activation_code = code


    def is_active(self):
        if self.is_student == True:
            self.is_active = False
            self.save(update_fields=['is_active'])


# class PasswordReset(models.Model):
#     email = models.EmailField()