from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAdmin(permissions.BasePermission):
    """
    Класс IsAdmin используется для определения соответствия роли пользователя
    отправившего запрос как "администратор".

    Родительский класс -- permissions.BasePermission.
    Переопределенные методы -- has_permission.
    """

    def has_permission(self, request, view):
        """Определить и вернуть право на поступивший запрос."""
        if bool(request.user and request.user.is_authenticated):
            return request.user.is_staff or request.user.is_superuser
        return False


class IsOwner(permissions.BasePermission):
    """
    Класс IsOwner используется для определения принадлежности запрашивоемой
    записи текущему пользователю.

    Родительский класс -- permissions.BasePermission.
    Переопределенные методы -- has_permission, has_object_permission.
    """

    def has_permission(self, request, view):
        """Определить и вернуть право на поступивший запрос."""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Определить и вернуть право на доступ к объекту."""
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if bool(request.user and request.user.is_authenticated):
            return request.user.is_staff or request.user.is_superuser


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
