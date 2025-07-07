from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permite que:
    - Los usuarios normales hagan CRUD solo sobre su propio objeto.
    - Los administradores puedan hacer CRUD sobre todos.
    """

    def has_object_permission(self, request, view, obj):
        # Admin puede hacer cualquier cosa
        if request.user.is_staff:
            return True

        # Usuario normal solo puede actuar sobre su propio objeto
        return obj.user == request.user
