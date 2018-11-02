from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from vie_quotidienne.models import *

admin.site.register(Culte)
admin.site.register(Emploi)
admin.site.register(SalleDeSpectacle)
admin.site.register(Hebergement)
admin.site.register(TypeHebergement)
admin.site.register(Cimetiere)
