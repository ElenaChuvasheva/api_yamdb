from rest_framework import permissions

from users.models import CustomUser


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """Разрешение, позволяющее добавлять, удалять и редактировать объекты
    только пользователям с правами администратора.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == CustomUser.ADMIN
            or request.user.role == CustomUser.MODERATOR
        )


class IsAdmin(permissions.BasePermission):
    """Разрешение, позволяющее производить действия с объектами
    только пользователям с правами администратора.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == CustomUser.ADMIN)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение, позволяющее добавлять и удалять объекты
    только пользователям с правами администратора.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == CustomUser.ADMIN
        )
