from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings

from api.permissions import UserIsHebergeurOrOwnerOrAdmin, UserIsCommercantOrOwnerOrAdmin, \
    UserIsPresidentOrSecretaryOrAdmin, UserIsPresidentOrSecretaryOfAssocOrAdmin
from association.serializers import *
from cadre_de_vie.serializers import *
from core.serializers import *
from vie_municipale.serializers import *
from vie_quotidienne.serializers import *


class MultiSerializerViewSet(viewsets.GenericViewSet):
    """
    MultiSerializerViewSet est une class custom permettant l'usage de plusieurs serializer
    en fonction de l'action.
    Elle permet aussi de sélectionner les permissions à accorder en fonction de l'action.
    """
    serializers = {
        'default': None,
    }

    permission_classes = {
        'default': api_settings.DEFAULT_PERMISSION_CLASSES,

    }

    def get_serializer_class(self):
        return self.serializers.get(self.action,
                                    self.serializers['default'])

    def get_permissions(self):
        permission_list = self.permission_classes.get(self.action,
                                                      self.permission_classes['default'])
        return [permission() for permission in permission_list]


class CrudViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    pass


class UploadedImageViewset(MultiSerializerViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                           mixins.DestroyModelMixin):
    queryset = UploadedImage.objects.all()
    permission_classes = {
        'default': (permissions.IsAuthenticatedOrReadOnly,),
    }
    serializers = {
        'default': UploadedImageDetailSerializer,
        'create': UploadedImageSerializer
    }
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('object_id', 'content_type')


class UserViewset(MultiSerializerViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = User.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': UserDetailSerializer,
        'list': UserSerializer,
        'retrieve': UserSerializer,
        'detail-full': UserDetailSerializer
    }

    @action(
        detail=True,
        methods=['post'],
        url_path='retrieve-full',
    )
    def retrieve_full(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CommissionViewset(MultiSerializerViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                        mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Commission.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': CommissionDetailSerializer,
        'list': CommissionSerializer,
        'create': CommissionCreateSerializer,
        'update': CommissionCreateSerializer,
        'partial_update': CommissionCreateSerializer,
    }


class BulletinViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Bulletin.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': BulletinSerializer,
    }


class ConseilViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Conseil.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': ConseilDetailSerializer,
        'list': ConseilSerializer
    }


class ServiceViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Service.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': ServiceDetailSerializer,
        'list': ServiceSerializer,
    }


class SalleDeFeteViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = SalleDeFete.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': SalleDeFeteDetailSerializer,
        'list': SalleDeFeteSerializer
    }


class HebergementViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Hebergement.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'create': (UserIsHebergeurOrOwnerOrAdmin,),
        'update': (UserIsHebergeurOrOwnerOrAdmin,),
        'partial_update': (UserIsHebergeurOrOwnerOrAdmin,),
        'destroy': (UserIsHebergeurOrOwnerOrAdmin,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': HebergementDetailSerializer,
        'list': HebergementSerializer,
        'create': HebergementCreateSerializer,
        'update': HebergementCreateSerializer,
        'partial_update': HebergementCreateSerializer,
    }


class CimetiereViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Cimetiere.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': CimetiereDetailSerializer,
        'list': CimetiereSerializer,
    }


class CommerceViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Commerce.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'create': (UserIsCommercantOrOwnerOrAdmin,),
        'update': (UserIsCommercantOrOwnerOrAdmin,),
        'partial_update': (UserIsCommercantOrOwnerOrAdmin,),
        'destroy': (UserIsCommercantOrOwnerOrAdmin,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': CommerceDetailSerializer,
        'list': CommerceSerializer,
        'create': CommerceCreateSerializer,
        'update': CommerceCreateSerializer,
        'partial_update': CommerceCreateSerializer,
    }


class MarcheViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Marche.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': MarcheDetailSerializer,
        'list': MarcheSerializer,
    }


class MarcheHoraireViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = MarcheHoraire.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': MarcheHoraireSerializer
    }


class AssociationViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Association.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'create': (UserIsPresidentOrSecretaryOrAdmin,),
        'update': (UserIsPresidentOrSecretaryOrAdmin,),
        'partial_update': (UserIsPresidentOrSecretaryOrAdmin,),
        'destroy': (UserIsPresidentOrSecretaryOrAdmin,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': AssociationDetailSerializer,
        'list': AssociationSerializer,
        'create': AssociationCreateSerializer,
        'update': AssociationCreateSerializer,
        'partial_update': AssociationCreateSerializer,
    }


class EvenementViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Evenement.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'create': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'update': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'partial_update': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'destroy': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': EvenementDetailSerializer,
        'list': EvenementSerializer,
        'create': EvenementCreateSerializer,
        'update': EvenementCreateSerializer,
        'partial_update': EvenementCreateSerializer,
    }


class PatrimoineViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Evenement.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': PatrimoineCreateSerializer,
        'list': PatrimoineSerializer,
        'retrieve': PatrimoineDetailSerializer
    }


class TravailViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Travail.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': TravailSerializer,
    }


class TerrainViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Terrain.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': TerrainSerializer,
    }


class DistinctionViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Distinction.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': DistinctionDetailSerializer,
        'list': DistinctionSerializer,
    }


class NewpaperViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Newpaper.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'create': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'update': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'partial_update': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'destroy': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }
    serializers = {
        'default': NewpaperDetailSerializer,
        'list': NewpaperSerializer,
        'create': NewpaperCreateSerializer,
        'update': NewpaperCreateSerializer,
        'partial_update': NewpaperCreateSerializer,
    }
