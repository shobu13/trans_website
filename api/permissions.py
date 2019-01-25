from django.contrib.auth.models import User
from django.forms import model_to_dict
from rest_framework import permissions
from rest_framework.request import Request

from cadre_de_vie.models import Evenement
from vie_quotidienne.models import Commerce, Hebergement
from association.models import Association


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


class UserIsPresidentOrSecretaryOrAdmin(permissions.IsAdminUser):
    message = ''

    def has_permission(self, request, view):
        self.message = 'User is not Admin'
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj: Association):
        self.message = 'User is not president or secretary of this object.'
        user: User = request.user
        return user == obj.president or user == obj.secretaire or user.is_superuser


class UserIsPresidentOrSecretaryOfAssocOrAdmin(permissions.IsAdminUser):
    message = ''

    def has_permission(self, request: Request, view):
        owner = Association.objects.get(id=request.data["owner"])
        self.message = 'User is not president or secretary of the owner of this object.'
        return request.user.is_superuser or request.user == owner.president or request.user == owner.secretaire

    def has_object_permission(self, request, view, obj: Evenement):
        self.message = 'User is not president or secretary of the owner of this object.'
        user: User = request.user
        return user == obj.owner.president or user == obj.owner.secretaire or user.is_superuser
