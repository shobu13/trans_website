from django.db import models

from markdownx.models import MarkdownxField


class Association(models.Model):
    """
    Modèle décrivant une association

    possède 3 clé étrangères en référence à :model:`auth.User` pour le president, le tresorier et
    secretaire.
    """
    nom = models.CharField(max_length=150)
    description = MarkdownxField()

    president = models.ForeignKey('auth.User', models.PROTECT,
                                  related_name='association_president')
    tresorier = models.ForeignKey('auth.User', models.PROTECT,
                                  related_name='association_tresorier')
    secretaire = models.ForeignKey('auth.User', models.PROTECT,
                                   related_name='association_secretaire')

    def __str__(self):
        return self.nom
