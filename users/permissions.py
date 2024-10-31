from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Сравниваем текущего пользователя с объектом
        return obj == request.user
