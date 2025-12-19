from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsNotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moderators").exists()


class IsModeratorOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="moderators").exists():
            return True
        return obj.owner == request.user


class IsModeratorOrCourseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="moderators").exists():
            return True
        return obj.owner == request.user
