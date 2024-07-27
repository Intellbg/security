from rest_framework import permissions

#Implementación de validaciones de permisos para el acceso restringido de recursos 
# en función del tipo de usuario
class IsAdministrator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.administrator.first()


class IsPasseStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsCheckpoint(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.checkpoint.first()
