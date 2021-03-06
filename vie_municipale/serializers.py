from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from core.serializers import UploadedImageSerializer
from vie_municipale.models import *


class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = ('id', 'titre',)
        depth = 0


class CommissionDetailSerializer(serializers.ModelSerializer):
    images = UploadedImageSerializer(many=True, read_only=True)

    class Meta:
        model = Commission
        fields = '__all__'
        depth = 1

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class CommissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = '__all__'

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class BulletinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bulletin
        fields = '__all__'


class ConseilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conseil
        fields = ('id', 'titre', 'date',)


class ConseilDetailSerializer(serializers.ModelSerializer):
    images = UploadedImageSerializer(many=True, read_only=True)

    class Meta:
        model = Conseil
        fields = '__all__'

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'titre',)


class ServiceDetailSerializer(serializers.ModelSerializer):
    images = UploadedImageSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)
