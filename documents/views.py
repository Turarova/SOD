from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .kundoluk_db import KundolukDbStudent
from .models import StudentDocument
from .permissions import IsDirector
from .serializers import StudentDocumentSerializer
from .tasks import parse_grades


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
