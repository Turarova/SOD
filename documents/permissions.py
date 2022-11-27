from rest_framework.permissions import BasePermission, SAFE_METHODS
from school.models import User

class IsDirector(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_student:
            return request.user


class IsStudentsDocument(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return not request.user.is_student or obj.users_inn == request.user