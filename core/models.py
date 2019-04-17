from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class EluPicture(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='elu_picture')
    picture = models.ImageField(upload_to='elus_pictures/', help_text='Rappel : Pour les élus uniquement.')

    def delete(self, using=None, keep_parents=False):
        self.picture.delete()
        return super().delete(using, keep_parents)


class EluRole(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='elu_role')
    name = models.CharField(max_length=100, help_text='Rappel : Pour les élus uniquement. Rôles disponibles : maire, adjoint1, adjoint2, adjoint3')
