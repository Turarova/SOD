from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .kundoluk_db import KundolukDbStudent
from .models import StudentDocument
from .serializers import StudentDocumentSerializer
from .permissions import IsDirector, IsStudentsDocument
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.decorators import action
from django.http import HttpResponse
from .permissions import IsDirector
from .serializers import StudentDocumentSerializer
from .tasks import parse_grades


class DocumentViewSet(ModelViewSet):
    queryset = StudentDocument.objects.all()
    serializer_class = StudentDocumentSerializer
    # search_fields = ['name', 'surname']

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permissions = [IsAuthenticated, IsDirector]
        else:
            permissions = [IsAuthenticated, IsStudentsDocument]
        return [permission() for permission in permissions]

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        print(self)
        print(request.query_params)
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(name__icontains=q) |
                                   Q(surname__icontains=q))
        serializer = StudentDocumentSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


def write_db(request):
    import csv
    import os
    open('db.csv', 'w').close()
    students = StudentDocument.objects.all()
    with open('db.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(('имя', 'фамилия', 'класс', 'годовая оценка'))
        for student in students:
            writer.writerow((student.name, student.surname, student.student_class, student.years_grade))
    with open('db.csv') as f:
        db = f.read()
    os.remove('db.csv')
    return HttpResponse(db, content_type='application/csv')
            

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
