from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # If the request is a GET, OPTIONS or HEAD, authorize the request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # If the request is a POST, PUT, PATCH or DELETE, ensure the request user matches the object owner
        print(obj)
        return obj == request.user or obj.get('owner') == request.user