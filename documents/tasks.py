from celery import shared_task
from rest_framework.response import Response

from .kundoluk_db import KundolukDbStudent
from .models import StudentDocument



@shared_task
def parse_grades():
    kundoluk = KundolukDbStudent.objects.using('kundoluk').all()
    students = StudentDocument.objects.all()

    for student in students:
        for k_student in kundoluk:
            if k_student.inn == student.users_inn.inn:
                student.quarters_1_grade = k_student.quarters_1_grade
                student.quarters_2_grade = k_student.quarters_2_grade
                student.quarters_3_grade = k_student.quarters_3_grade
                student.quarters_4_grade = k_student.quarters_4_grade
                student.years_grade = k_student.years_grade
                student.save()
                break

    # return Response('ok')