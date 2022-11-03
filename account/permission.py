from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allows access only to authenticated users and requestd user has admin role.
    """

    def has_permission(self, request, view):
        user = request.user.role.all().values_list('name', flat=True)
        return bool('admin' in user and request.user.is_authenticated)