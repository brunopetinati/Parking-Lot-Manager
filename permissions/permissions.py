from rest_framework import permissions

class AdminAuthorization(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_superuser

        else:
            # rota get incluída aqui
            return True