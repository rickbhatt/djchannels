from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsUnauthenticated(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return True

        raise PermissionDenied("Access denied as the user is athenticated")
