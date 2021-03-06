from django.contrib.contenttypes.fields import GenericRelation
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
                                  related_name='president')
    tresorier = models.ForeignKey('auth.User', models.PROTECT,
                                  related_name='tresorier')
    secretaire = models.ForeignKey('auth.User', models.PROTECT,
                                   related_name='secretaire')

    cover = models.ImageField(upload_to="uploaded_images/association/", null=True)

    images = GenericRelation('core.UploadedImage')

    def delete(self, using=None, keep_parents=False):
        self.cover.delete()
        super().delete()

    def __str__(self):
        return self.nom
