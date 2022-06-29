from rest_framework import permissions

class UserPermissionsCustom(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if "is_active" in request.data:
            return False

        if obj.id == request.user.id:
            return True
