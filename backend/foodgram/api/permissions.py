from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorPermission(BasePermission):
    """Только автор может изменять и добавлять объект."""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)
