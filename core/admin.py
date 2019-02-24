from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from core.models import *


class EluPictureInline(admin.StackedInline):
    model = EluPicture


class EluRoleInline(admin.StackedInline):
    model = EluRole


class UserAdmin(BaseUserAdmin):
    inlines = (EluPictureInline, EluRoleInline,)


admin.site.register(UploadedImage)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
