from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from vie_quotidienne.models import *

admin.site.register(SalleDeFete)
admin.site.register(Hebergement)
admin.site.register(TypeHebergement)
admin.site.register(Cimetiere)
admin.site.register(Marche)
