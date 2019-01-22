from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from vie_quotidienne.models import *


class SalleDeFeteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalleDeFete
        fields = ('id', 'nom', 'adresse',)


class SalleDeFeteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalleDeFete
        fields = '__all__'

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class TypeHebergementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeHebergement
        fields = '__all__'


class HebergementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hebergement
        fields = ('id', 'nom', 'adresse', 'type')


class HebergementDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hebergement
        fields = '__all__'
        depth = 1

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class HebergementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hebergement
        fields = '__all__'

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class CimetiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cimetiere
        fields = ('id', 'nom', 'adresse',)


class CimetiereDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cimetiere
        fields = '__all__'
        depth = 1

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class CommerceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commerce
        fields = ('id', 'nom', 'adresse',)


class CommerceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commerce
        fields = '__all__'
        depth = 1

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class CommerceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commerce
        fields = '__all__'

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)


class MarcheHoraireSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarcheHoraire
        fields = '__all__'


class MarcheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marche
        fields = ('id', 'adresse')


class MarcheDetailSerializer(serializers.ModelSerializer):
    marchehoraire_set = MarcheHoraireSerializer(many=True)

    class Meta:
        model = Marche
        fields = ('id', 'adresse', 'marchehoraire_set', 'content_type')

    content_type = serializers.CharField(read_only=True,
                                         default=ContentType.objects.get_for_model(Meta.model).id)
