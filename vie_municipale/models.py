from django.db import models


class Commission(models.Model):
    titre = models.CharField(max_length=250)
