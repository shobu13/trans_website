from django.db import models

from markdownx.models import MarkdownxField


class Culte(models.Model):
    """
    Modele representant un culte
    le nom est limite a 150 caractere
    """
    nom = models.CharField(max_length=150)
    texte = models.TextField()


class Emploi(models.Model):
    """
    Modele representant un emploi
    le titre est limite a 250 caractere
    """
    titre = models.CharField(max_length=250)
    description = models.TextField()
    remuneration = models.FloatField()


class SalleDeSpectacle(models.Model):
    """
    modele representant une salle de spectacle
    le champ description supporte le markdown et servira à donner diverses infos.
    """
    nom = models.CharField(max_length=150)
    adresse = models.CharField(max_length=250)
    description = MarkdownxField()


class Hebergement(models.Model):
    """
    modele representant un hebergement pouvant etre un gite ou autre
    possede un champ description afin de donner les informations tel que le prix, ainsi qu'une cle
    etrangere vers le modele :model:`vie_quotidienne.TypeHebergement`
    """
    nom = models.CharField(max_length=150)
    adresse = models.CharField(max_length=250)
    description = models.TextField()
    type = models.ForeignKey('TypeHebergement', on_delete=models.PROTECT)


class TypeHebergement(models.Model):
    """
    modele representant un type d'hebergement
    """
    libelle = models.CharField(max_length=100)


class Cimetiere(models.Model):
    """
    modele representant un cimetiere
    """
    nom = models.CharField(max_length=150)
    adresse = models.CharField(max_length=250)
    description = MarkdownxField()


class Commerce(models.Model):
    nom = models.CharField(max_length=150)
    description = MarkdownxField()
