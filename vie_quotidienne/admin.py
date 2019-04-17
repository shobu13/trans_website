from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from vie_quotidienne.models import *


class MarcheHoraireInline(admin.TabularInline):
    model = MarcheHoraire
    extra = 0


class MarcheAdmin(admin.ModelAdmin):
    model = Marche
    inlines = (MarcheHoraireInline,)


admin.site.register(SalleDeFete)
admin.site.register(Hebergement)
admin.site.register(TypeHebergement)
admin.site.register(Cimetiere)
admin.site.register(Marche, MarcheAdmin)
admin.site.register(Commerce)
