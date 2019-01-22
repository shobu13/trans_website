from django.contrib import admin

from cadre_de_vie.models import *


class PatrimoineImageInline(admin.TabularInline):
    model = PatrimoineImage


class PatrimoineAdmin(admin.ModelAdmin):
    inlines = [PatrimoineImageInline, ]


admin.site.register(Patrimoine, PatrimoineAdmin)
admin.site.register(Distinction)
admin.site.register(Evenement)
admin.site.register(Newpaper)
admin.site.register(Terrain)
admin.site.register(Travail)
