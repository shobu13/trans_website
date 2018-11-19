from django.db import models

from markdownx.models import MarkdownxField


class Association(models.Model):
    """
    Modèle décrivant une association

    possède 3 clé étrangères en référence à :model:`auth.User` pour le president, le tresorier et
    secretaire.
    """
    description = MarkdownxField()

    president = models.ForeignKey('auth.User', models.PROTECT,
                                  related_name='Association_president_set')
    tresorier = models.ForeignKey('auth.User', models.PROTECT,
                                  related_name='Association_tresorier_set')
    secretaire = models.ForeignKey('auth.User', models.PROTECT,
                                   related_name='Association_secretaire_set')
