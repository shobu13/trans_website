from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from association.serializers import AssociationSerializer
from cadre_de_vie.models import *
from core.serializers import UploadedImageSerializer


class EvenementSerializer(serializers.ModelSerializer):
    owner = AssociationSerializer(read_only=True)

    class Meta:
        model = Evenement
        fields = ('nom', 'est_mairie', 'owner')


class EvenementDetailSerializer(serializers.ModelSerializer):
    images = UploadedImageSerializer(many=True, read_only=True)

    class Meta:
        model = Evenement
        fields = '__all__'
        depth = 1

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class EvenementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evenement
        fields = '__all__'

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class PatrimoineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patrimoine
        fields = ('nom', 'adresse', 'patrimoine_image')


class PatrimoineDetailSerializer(serializers.ModelSerializer):
    images = UploadedImageSerializer(many=True, read_only=True)

    class Meta:
        model = Patrimoine
        fields = '__all__'
        depth = 1

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class PatrimoineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patrimoine
        fields = '__all__'

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class TravailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patrimoine
        fields = '__all__'


class TerrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terrain
        fields = '__all__'


class DistinctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distinction
        fields = ('nom', 'date',)


class DistinctionDetailSerializer(serializers.ModelSerializer):
    images = UploadedImageSerializer(many=True, read_only=True)

    class Meta:
        model = Distinction
        fields = '__all__'
        depth = 1

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class NewpaperSerializer(serializers.ModelSerializer):
    owner = AssociationSerializer(read_only=True)

    class Meta:
        model = Newpaper
        fields = ('titre', 'date', 'est_mairie', 'owner')


class NewpaperDetailSerializer(serializers.ModelSerializer):
    images = UploadedImageSerializer(many=True, read_only=True)

    class Meta:
        model = Newpaper
        fields = '__all__'
        depth = 1

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class NewpaperCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newpaper
        fields = '__all__'

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)
