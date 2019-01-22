from django.contrib.auth.models import User
from rest_framework import permissions

from vie_quotidienne.models import Commerce, Hebergement


class UserIsHebergeurOrOwnerOrAdmin(permissions.IsAdminUser):
    message = ''

    def has_permission(self, request, view):
        self.message = 'User not in Group Hebergeur'
        user: User = request.user
        return user.groups.filter(name="Hebergeur") or super().has_permission(request, view)

    def has_object_permission(self, request, view, obj: Hebergement):
        self.message = 'User is not owner of this object.'
        user: User = request.user
        return user == obj.owner or user.is_superuser


class UserIsCommercantOrOwnerOrAdmin(permissions.IsAdminUser):
    message = ''

    def has_permission(self, request, view):
        self.message = 'User not in Group Commercant'
        user: User = request.user
        return user.groups.filter(name="Commercant") or super().has_permission(request, view)

    def has_object_permission(self, request, view, obj: Commerce):
        self.message = 'User is not owner of this object.'
        user: User = request.user
        return user == obj.owner or user.is_superuser
