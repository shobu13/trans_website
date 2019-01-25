from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from association.models import *
from core.serializers import UploadedImageSerializer


class AssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        fields = ('nom', 'president')


class AssociationDetailSerializer(serializers.ModelSerializer):
    images = UploadedImageSerializer(many=True, read_only=True)

    class Meta:
        model = Association
        fields = '__all__'
        depth = 1

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class AssociationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        fields = '__all__'
