from rest_framework import permissions

class HasRolePermission(permissions.BasePermission):
    """
    Ensures user belongs to the organization and checks authorization role layers.
    """
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # User must belong to an organization
        if not request.user.organization:
            return False
            
        return request.user.role in self.allowed_roles

class IsAnalystOrAbove(HasRolePermission):
    def __init__(self):
        super().__init__(['OWNER', 'ADMIN', 'ANALYST'])

class IsViewerOrAbove(HasRolePermission):
    def __init__(self):
        super().__init__(['OWNER', 'ADMIN', 'ANALYST', 'VIEWER'])