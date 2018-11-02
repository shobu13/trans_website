from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from vie_municipale.models import *


class BulletinModelAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        """
        Surcharge de la fonction delete_queryset permettant de supprimer les éléments d'un queryset,
        cette surcharge permet de supprimer aussi chaque fichier pdf associé à chaque objet.
        :param request:
        :param queryset:
        :return:
        """
        for bulletin_model in queryset:
            assert isinstance(bulletin_model, Bulletin)
            bulletin_model.pdf.delete()
        super().delete_queryset(request, queryset)


class CommissionModelAdmin(MarkdownxModelAdmin):
    filter_horizontal = ('titulaires', 'suppleants', )


admin.site.register(Commission, CommissionModelAdmin)
admin.site.register(Bulletin, BulletinModelAdmin)
admin.site.register(Conseil)
admin.site.register(Service)
