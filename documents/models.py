from django.db import models
from phonenumber_field.modelfields import PhoneNumberField



class Counselor(models.Model):
    SCHOOL_CHOICES = (
        ('1', 'Аламединская 1'),
        ('38', '38 Гимназия'),
        ('Айчурок', 'Айчурок'),
        ('61', '61 школа'),
        ('67', '67 школа гимназия')
    )

    # date_of_birth = models.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])
    date_of_birth = models.DateField(blank=True, null=True)
    school_name = models.CharField(max_length=100, choices=SCHOOL_CHOICES, blank=True, null=True)
    students_inn = models.CharField(max_length=15, unique=True, blank=True, null=True)
    guardians_name = models.CharField(max_length=255, blank=True, null=True)
    guardians_surname = models.CharField(max_length=255, blank=True, null=True)
    guardians_number = PhoneNumberField(blank=True, null=True)
    guardians_inn = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    surname = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    characteristic = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='students_image', blank=True, null=True)
    inn = models.CharField(max_length=15, unique=True, blank=True, null=True)
    nation = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.inn}"

class StudentDocument(models.Model):

    inn = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    student_class = models.CharField(max_length=10, blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)
    subject = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.inn} {self.student_class}"