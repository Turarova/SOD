from django.db import models
from school.models import School


class Counselor(models.Model):
    SCHOOL_CHOICES = (
        ('1', 'Аламединская 1'),
        ('38', '38 Гимназия'),
        ('Айчурок', 'Айчурок'),
        ('61', '61 школа'),
        ('67', '67 школа гимназия')
    )

    date_of_birth = models.DateField()
    school_name = models.CharField(max_length=7, choices=SCHOOL_CHOICES)
    students_inn = models.CharField(max_length=15, unique=True)
    guardians_name = models.CharField(max_length=255)
    guardians_surname = models.CharField(max_length=255)
    guardians_number = models.IntegerField()
    guardians_inn = models.CharField(max_length=255)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    characteristic = models.TextField()
    image = models.ImageField(upload_to='students_image')
    inn = models.CharField(max_length=15, unique=True)
    nation = models.CharField(max_length=20)


class StudentDocument(models.Model):

    inn = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    student_class = models.CharField(max_length=10)
    grade = models.IntegerField()
    subject = models.CharField(max_length=50)