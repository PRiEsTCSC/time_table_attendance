from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'teacher'

class IsAdminOrTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in ['admin', 'teacher']
