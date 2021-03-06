from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from markdownx.models import MarkdownxField


class SalleDeFete(models.Model):
    """
    modele representant une salle de Fete
    le champ description supporte le markdown et servira à donner diverses infos.
    """
    nom = models.CharField(max_length=150)
    adresse = models.CharField(max_length=250)
    description = MarkdownxField()

    images = GenericRelation('core.UploadedImage')

    def __str__(self):
        return self.nom


class Hebergement(models.Model):
    """
    modele representant un hebergement pouvant etre un gite ou autre
    possede un champ description afin de donner les informations tel que le prix, ainsi qu'une cle
    etrangere vers le modele :model:`vie_quotidienne.TypeHebergement`
    """
    nom = models.CharField(max_length=150)
    adresse = models.CharField(max_length=250)
    description = models.TextField()
    resume = models.CharField(max_length=280)
    header = models.ImageField(upload_to='hebergement_header/', null=True)

    type = models.ForeignKey('TypeHebergement', on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    images = GenericRelation('core.UploadedImage')

    def __str__(self):
        return self.nom


class TypeHebergement(models.Model):
    """
    modele representant un type d'hebergement
    """
    libelle = models.CharField(max_length=100)

    def __str__(self):
        return self.libelle


class Cimetiere(models.Model):
    """
    modele representant un cimetiere
    """
    nom = models.CharField(max_length=150)
    adresse = models.CharField(max_length=250)
    code_postal = models.CharField(max_length=5)
    description = MarkdownxField()

    images = GenericRelation('core.UploadedImage')

    def __str__(self):
        return self.nom


class Commerce(models.Model):
    nom = models.CharField(max_length=150)
    adresse = models.CharField(max_length=250)
    code_postal = models.CharField(max_length=5)
    resume = models.CharField(max_length=280)
    description = MarkdownxField()
    header = models.ImageField(upload_to='commerces_header/')

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    images = GenericRelation('core.UploadedImage')

    def __str__(self):
        return self.nom


class Marche(models.Model):
    adresse = models.CharField(max_length=250)
    code_postal = models.CharField(max_length=5)

    def __str__(self):
        return self.adresse


class MarcheHoraire(models.Model):
    jour = models.CharField(choices=(
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi'),
        ('Dimanche', 'Dimanche'),
    ), max_length=10)
    debut = models.TimeField()
    fin = models.TimeField()

    marche = models.ForeignKey('Marche', on_delete=models.CASCADE, related_name="horaires")

    def __str__(self):
        return "{} le {}".format(self.marche.adresse, str(self.jour))
