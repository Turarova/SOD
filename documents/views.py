from rest_framework.viewsets import ModelViewSet
from .models import StudentDocument
from .serializers import Counselor

class DocumentViewSet(ModelViewSet):
    queryset = StudentDocument.objects.all()
    serializer_class = Counselor