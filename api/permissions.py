from rest_framework import permissions


class IsCreator(permissions.BasePermission):
    """
    Object-level permissions for the creator of the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            return obj.creator == request.user


class IsCreatorOrExecutor(permissions.BasePermission):
    """
    Object-level permission to determine allowed methods depending
    on the creator/executor status.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PATCH']:
            return obj.executor == request.user or obj.creator == request.user
        elif request.method == ['DELETE', 'PUT']:
            return obj.creator == request.user
