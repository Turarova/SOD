from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsDirector(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return request.user.is_staff