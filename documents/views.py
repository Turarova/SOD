from rest_framework.viewsets import ModelViewSet
from .models import StudentDocument
from .serializers import StudentDocumentSerializer
from .permissions import IsDirector, IsStudentsDocument
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.decorators import action
from django.http import HttpResponse

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