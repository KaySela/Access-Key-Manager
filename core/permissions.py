from rest_framework import permissions 

class IsAdminOrPostReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST','GET'] and request.user.is_authenticated:
            return True
        return bool(request.user and request.user.is_staff)
    


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET'] and request.user.is_authenticated:
            return True
        return bool(request.user and request.user.is_staff)
    