from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from markdownx.models import MarkdownxField
from django.utils import timezone


class Evenement(models.Model):
    nom = models.CharField(max_length=150)
    description = MarkdownxField()
    est_mairie = models.BooleanField(default=False)

    owner = models.ForeignKey('association.Association', on_delete=models.PROTECT, null=True)
    images = GenericRelation('core.UploadedImage')

    def __str__(self):
        return self.nom


class Patrimoine(models.Model):
    nom = models.CharField(max_length=150)
    description = MarkdownxField()
    adresse = models.CharField(max_length=250)

    patrimoine_image = models.ImageField(upload_to='patrimoine_images/')
    images = GenericRelation('core.UploadedImage')

    def delete(self, using=None, keep_parents=False):
        """
        Surcharge de la fonction delete servant à supprimer l'objet, ici, on y supprime aussi
        l'image associée.
        :param using:
        :param keep_parents:
        :return:
        """
        self.patrimoine_image.delete()
        return super().delete(using, keep_parents)

    def __str__(self):
        return self.nom


class Travail(models.Model):
    """Travail de voirie, ect..."""

    class Meta:
        verbose_name_plural = 'Travaux'

    nom = models.CharField(max_length=150)
    adresse = models.CharField(max_length=250)
    duree = models.DurationField()

    def __str__(self):
        return '{}, {}'.format(self.nom, self.adresse)


class Terrain(models.Model):
    adresse = models.CharField(max_length=250)
    prix = models.FloatField()
    surface = models.FloatField()

    def __str__(self):
        return self.adresse


class Distinction(models.Model):
    nom = models.CharField(max_length=150)
    description = MarkdownxField()
    date = models.DateField()

    def __str__(self):
        return '{} le {}'.format(self.nom, self.date)


class Newpaper(models.Model):
    titre = models.CharField(max_length=150)
    texte = MarkdownxField()
    date = models.DateField(default=timezone.now)
    est_mairie = models.BooleanField()

    owner = models.ForeignKey('association.Association', on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.owner is None:
            return "{} de {}".format(self.titre, 'mairie')
        else:
            return "{} de {}".format(self.titre, self.owner.nom)

    # TODO étant donner le système d'upload, tout les model utilisant l'upload d'image doivent
    #  être créer avant l'édition du texte et démarrent donc avec un texte Null ou vide.
