from django.db import models

from markdownx.models import MarkdownxField


class Commission(models.Model):
    """
    Modele definissant une commission
    """
    titre = models.CharField(max_length=250)
    description = MarkdownxField()

    titulaires = models.ManyToManyField('auth.User', related_name='Commission_titulaire_set')
    suppleants = models.ManyToManyField('auth.User', related_name='Commission_suppleants_set')

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
    date = models.DateField()

    def __str__(self):
        return "{} - {}".format(self.titre, str(self.date))


class Service(models.Model):
    """Model definissant un Service"""
    titre = models.CharField(max_length=250)
    texte = MarkdownxField()

    def __str__(self):
        return self.titre
