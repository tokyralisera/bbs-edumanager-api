from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Permission personnalisée pour vérifier si l'utilisateur est admin"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'


class IsScolarite(permissions.BasePermission):
    """Permission personnalisée pour vérifier si l'utilisateur est du service scolarité"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'SCOLARITE'


class IsAdminOrScolarite(permissions.BasePermission):
    """Permission pour admin ou scolarité"""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['ADMIN', 'SCOLARITE']
        )