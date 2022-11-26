from rest_framework.viewsets import ModelViewSet
from .models import StudentDocument
from .serializers import StudentDocumentSerializer
from .permissions import IsDirector
from rest_framework.permissions import IsAuthenticated

class DocumentViewSet(ModelViewSet):
    queryset = StudentDocument.objects.all()
    serializer_class = StudentDocumentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permissions = [IsDirector, ]
        else:
            permissions = [IsAuthenticated, ]
        return [permission() for permission in permissions]