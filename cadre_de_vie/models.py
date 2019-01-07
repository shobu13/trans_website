from django.db import models
from markdownx.models import MarkdownxField
from django.utils import timezone


class Evenement(models.Model):
    nom = models.CharField(max_length=150)
    description = MarkdownxField()
    est_mairie = models.BooleanField(default=False)


class Patrimoine(models.Model):
    nom = models.CharField(max_length=150)
    description = MarkdownxField()
    adresse = models.CharField(max_length=250)

    def __str__(self):
        return self.nom


class PatrimoineImage(models.Model):
    image = models.ImageField(upload_to='patrimoine_images/')
    patrimoine = models.ForeignKey('Patrimoine', on_delete=models.CASCADE)

    def delete(self, using=None, keep_parents=False):
        """
        Surcharge de la fonction delete servant à supprimer l'objet, ici, on y supprime aussi
        l'image associée.
        :param using:
        :param keep_parents:
        :return:
        """
        self.image.delete()
        return super().delete(using, keep_parents)


class Travail(models.Model):
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


class New(models.Model):
    titre = models.CharField(max_length=150)
    text = MarkdownxField()
    date = models.DateField(default=timezone.now())
    est_mairie = models.BooleanField()

    models.ForeignKey('Association', on_delete=models.CASCADE)

    def __str__(self):
        return self.titre