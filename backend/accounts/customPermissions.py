from rest_framework import permissions

class IsSuperUserOrManager(permissions.BasePermission):
    """
    Custom permission: only superusers or managers 
    """
    def has_permission(self, request, view):
        return bool(
            request.user and (
                request.user.is_superuser or getattr(request.user, 'isManager', False)
            )
        )




class IsSuperUser(permissions.BasePermission):
    """
    Custom permission: Only super user can run this function
    """

    def has_permission(self, request, view):
        return bool(
            request.user and (
                request.user.is_superuser
            )
        )
    

# from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Only admins can modify, others can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff
