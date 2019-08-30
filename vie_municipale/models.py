from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone

from markdownx.models import MarkdownxField


class Commission(models.Model):
    """
    Modele definissant une commission
    """
    titre = models.CharField(max_length=250)
    description = MarkdownxField()

    titulaires = models.ManyToManyField('auth.User', related_name='commission_titulaire')
    suppleants = models.ManyToManyField('auth.User', related_name='commission_suppleants', blank=True)

    images = GenericRelation('core.UploadedImage')

    def __str__(self):
        return self.titre


class Bulletin(models.Model):
    """
    Modele definissant un bulletin
    """
    date = models.DateField()
    pdf = models.FileField(upload_to='bulletins/', )

    def delete(self, using=None, keep_parents=False):
        """
        Surcharge de la fonction delete servant à supprimer l'objet, ici, on y supprime aussi le
        fichier PDF associer.
        :param using:
        :param keep_parents:
        :return:
        """
        self.pdf.delete()
        return super().delete(using, keep_parents)

    def __str__(self):
        return str(self.date)


class Conseil(models.Model):
    """Modele definissant un Conseil"""
    titre = models.CharField(max_length=250)
    texte = MarkdownxField()
    pdf = models.FileField(upload_to='conseil_pdf/')
    date = models.DateField()

    images = GenericRelation('core.UploadedImage')

    def __str__(self):
        return "{} - {}".format(self.titre, str(self.date))


class Service(models.Model):
    """Model definissant un Service"""
    titre = models.CharField(max_length=250)
    texte = MarkdownxField()

    images = GenericRelation('core.UploadedImage')

    def __str__(self):
        return self.titre
