from django.db import models
from school.models import Students

class StudentDocument(models.Model):
    SCHOOL_CHOICES = (
        ('1', 'Аламединская 1'),
        ('38', '38 Гимназия'),
        ('Айчурок', 'Айчурок'),
        ('61', '61 школа'),
        ('67', '67 школа гимназия')
    )

    date_of_birth = models.DateField(null=True)
    school_name = models.CharField(max_length=255, choices=SCHOOL_CHOICES, blank=True, null=True)
    students_inn = models.CharField(max_length=15, unique=True, blank=True, null=True)
    guardians_name = models.CharField(max_length=255, blank=True, null=True)
    guardians_surname = models.CharField(max_length=255, blank=True, null=True)
    guardians_number = models.IntegerField(blank=True, null=True)
    guardians_inn = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    surname = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    characteristic = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True) #upload_to='students_image',
    nation = models.CharField(max_length=20, blank=True, null=True)
    counselors_inn = models.CharField(max_length=15, unique=True, blank=True, null=True)
    users_inn = models.ForeignKey(Students, on_delete=models.CASCADE, blank=True, null=True)
    student_class = models.CharField(max_length=10, blank=True, null=True)
    quarters_1_grade = models.IntegerField( blank=True,null=True)
    quarters_2_grade = models.IntegerField( blank=True,null=True)
    quarters_3_grade = models.IntegerField( blank=True,null=True)
    quarters_4_grade = models.IntegerField( blank=True,null=True)
    years_grade = models.IntegerField( blank=True,null=True)
    subject = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.surname} {self.name} {self.users_inn}'