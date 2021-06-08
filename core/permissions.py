from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsTheOwnerOf(BasePermission):
    """
        Allow access to object only to the owner
    """

    def has_object_permission(self, request, view, object):
        return bool(request.user.id == object.owner.id)
