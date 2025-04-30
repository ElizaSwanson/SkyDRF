from rest_framework import permissions


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.groups.filter(name="moderators").exists()
            or request.user.is_staff
        )
