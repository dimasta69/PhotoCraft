from rest_framework.permissions import BasePermission


class IsAuthenticatedAndIsPostRequest(BasePermission):
    def has_permission(self, request, view):
        if request.method in {'POST', "PUT", 'DELETE'}:
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if obj.user_id == request.user and obj.status != 'Published':
            return True

        return False
