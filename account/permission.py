from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):

        return bool(request.user.role.name == 'admin' and request.user.is_authenticated)