from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import UploadedImage


class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = '__all__'
        depth = 0


class UploadedImageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = '__all__'
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'email', 'groups', 'is_staff', 'is_superuser')
        depth = 1


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1
