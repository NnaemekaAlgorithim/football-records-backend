from rest_framework import permissions


class IsSuperAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superadmins to create or edit a league.
    Everyone else can only view (read-only access).
    """
    def has_permission(self, request, view):
        # Allow read-only access for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only allow superadmins to create or update
        return request.user.is_authenticated and request.user.is_superuser


class IsSuperAdminOrDenyDelete(permissions.BasePermission):
    """
    Custom permission to only allow superadmins to delete.
    Everyone else can create, update, and view.
    """
    def has_permission(self, request, view):
        # Allow everyone to view, create, and update (except delete)
        if request.method in ['DELETE']:
            # Only allow delete if the user is superadmin
            return request.user.is_authenticated and request.user.is_superuser
        return request.user.is_authenticated  # Allow others to create, update, and view
