from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from school.models import School

from .kundoluk_db import KundolukDbStudent
from .models import StudentDocument
from .permissions import IsDirector
from .serializers import StudentDocumentSerializer
from .tasks import parse_grades

User = get_user_model()


class DocumentViewSet(ModelViewSet):
    queryset = StudentDocument.objects.all()
    serializer_class = StudentDocumentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permissions = [IsDirector, ]
        else:
            permissions = [IsAuthenticated, ]
        return [permission() for permission in permissions]

@api_view(['GET'])
def parse_grades(request):
    parse_grades.delay()
    # kundoluk = KundolukDbStudent.objects.using('kundoluk').all()
    # students = StudentDocument.objects.all()

    # for student in students:
    #     for k_student in kundoluk:
    #         if k_student.inn == student.users_inn.inn:
    #             student.quarters_1_grade = k_student.quarters_1_grade
    #             student.quarters_2_grade = k_student.quarters_2_grade
    #             student.quarters_3_grade = k_student.quarters_3_grade
    #             student.quarters_4_grade = k_student.quarters_4_grade
    #             student.years_grade = k_student.years_grade
    #             student.save()
    #             break
    
    # return Response('ok')

# @api_view(['GET'])
# def school_rating(request):
#     schools = School.objects.all()
#     users = User.objects.all()
#     if 


#     return Response('ok')

@api_view(['GET'])
def students_rating(request):
    schools = School.objects.all()
    students = StudentDocument.objects.all()
    top = []
    for student in students:
        gpa = f'{student.users_inn.inn} {student.years_grade}'
        top.append(gpa)
    
    top.sort(reverse=True)

    return Response(top)

@api_view(['GET'])
def schools_rating(request):
    grades = []
    schools = School.objects.all()
    students = StudentDocument.objects.all()

    for student in students:
        grades.append(student.years_grade)
    
    average_rating = sum(grades) // len(grades)

    return Response(average_rating)


        
    