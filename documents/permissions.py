from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsDirector(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT','PATCH','DELETE','HEAD','OPTIONS']:
            return request.user.is_staff


class IsStudentsDocument(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("OBJ", obj)
        print("VIEW",view)
        if request.method == 'GET':
            return request.user.is_staff or obj.user == request.user