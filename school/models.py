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


class Director(AbstractUser):

    SCHOOL_CHOICES = (
        ('1', 'Аламединская 1'),
        ('38', '38 Гимназия'),
        ('Айчурок', 'Айчурок'),
        ('61', '61 школа'),
        ('67', '67 школа гимназия')
    )

    date_of_birth = models.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])
    school_name = models.CharField(max_length=1, choices=SCHOOL_CHOICES)
    students_inn = models.CharField(max_length=15, unique=True)
    guardians_name = models.CharField(max_length=255)
    guardians_surname = models.CharField(max_length=255)
    guardians_number = models.IntegerField(max_length=12)
    guardians_inn = models.CharField(max_length=255)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    characteristic = models.TextField()
    image = models.ImageField(upload_to='students_image')
    inn = models.CharField(max_length=15, unique=True)
    nation = models.CharField(max_length=20)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email





class Students(AbstractUser):
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField('email address', unique=True)
    password = models.CharField(max_length=100)
    inn = models.CharField(max_length=15, unique=True) 
    is_active = models.BooleanField('active', default=False)
    activation_code = models.CharField(max_length=36, blank=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


    def activate_with_code(self, code):
        if str(self.activation_code) != str(code):
            raise Exception(('code does not match'))
        self.is_active = True
        self.activation_code = ''
        self.save(update_fields=['is_active', 'activation_code'])

    def create_activation_code(self):
        code = str(uuid.uuid4())
        self.activation_code = code









class PasswordReset(models.Model):
    email = models.EmailField()