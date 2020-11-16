from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Предоставляет права на редактирование или удаление только владельцу или админу
    """

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or request.user.is_staff

