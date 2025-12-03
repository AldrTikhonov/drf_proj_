from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором."""
    message = "Доступ только модераторам."

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем"""
    message = "Доступ только владельцам"

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False