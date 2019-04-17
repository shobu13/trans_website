from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, mixins, status
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


class FilterDateInterval(viewsets.GenericViewSet):
    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        first_date: str = self.request.query_params.get('first_date', None)
        last_date: str = self.request.query_params.get('last_date', None)

        if first_date:
            year, month, day = first_date.split('-')
            first_date: datetime = datetime(int(year), int(month), int(day))
        if last_date:
            year, month, day = last_date.split('-')
            last_date: datetime = datetime(int(year), int(month), int(day))
        if first_date and last_date:
            queryset = queryset.filter(date__range=(first_date, last_date))

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset


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


class ListRetrieveViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin):
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


class UserViewset(MultiSerializerViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': UserDetailSerializer,
        'list': UserSerializer,
        'retrieve': UserSerializer,
        'detail_full': UserDetailSerializer,
        'list_elected': UserSerializer
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

    @action(
        detail=False,
        methods=['get'],
        url_path='list-elected',
    )
    def list_elected(self, request, *args, **kwargs):
        response = {}
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        try:
            response['maire'] = self.get_serializer(queryset.get(elu_role__name='maire'), many=False).data
        except:
            pass
        try:
            response['adjoint1'] = self.get_serializer(queryset.get(elu_role__name='adjoint1'), many=False).data
        except:
            pass
        try:
            response['adjoint2'] = self.get_serializer(queryset.get(elu_role__name='adjoint2'), many=False).data
        except:
            pass
        try:
            response['adjoint3'] = self.get_serializer(queryset.get(elu_role__name='adjoint3'), many=False).data
        except:
            pass
        response['conseillers'] = self.get_serializer(queryset.filter(elu_role__name='conseiller'), many=True).data
        return Response(response)


class CommissionViewset(MultiSerializerViewSet, ListRetrieveViewSet, FilterDateInterval):
    queryset = Commission.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': CommissionDetailSerializer,
        'list': CommissionSerializer,
        'create': CommissionCreateSerializer,
        'update': CommissionCreateSerializer,
        'partial_update': CommissionCreateSerializer,
    }


class BulletinViewset(MultiSerializerViewSet, ListRetrieveViewSet, FilterDateInterval):
    queryset = Bulletin.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': BulletinSerializer,
    }


class ConseilViewset(MultiSerializerViewSet, ListRetrieveViewSet, FilterDateInterval):
    queryset = Conseil.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': ConseilDetailSerializer,
        'list': ConseilSerializer
    }


class ServiceViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = Service.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': ServiceDetailSerializer,
        'list': ServiceSerializer,
    }


class SalleDeFeteViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = SalleDeFete.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': SalleDeFeteDetailSerializer,
        'list': SalleDeFeteDetailSerializer,
        # TODO a modifier quand d'autres salles serons construites, revoir design du site par l'occasion.
        # 'list': SalleDeFeteSerializer
    }


class HebergementViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = Hebergement.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),
        'create': (UserIsHebergeurOrOwnerOrAdmin,),
        'update': (UserIsHebergeurOrOwnerOrAdmin,),
        'partial_update': (UserIsHebergeurOrOwnerOrAdmin,),
        'destroy': (UserIsHebergeurOrOwnerOrAdmin,),

    }
    serializers = {
        'default': HebergementDetailSerializer,
        'list': HebergementSerializer,
        'create': HebergementCreateSerializer,
        'update': HebergementCreateSerializer,
        'partial_update': HebergementCreateSerializer,
    }


class CimetiereViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = Cimetiere.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': CimetiereDetailSerializer,
        'list': CimetiereSerializer,
    }


class CommerceViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = Commerce.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),
        'create': (UserIsCommercantOrOwnerOrAdmin,),
        'update': (UserIsCommercantOrOwnerOrAdmin,),
        'partial_update': (UserIsCommercantOrOwnerOrAdmin,),
        'destroy': (UserIsCommercantOrOwnerOrAdmin,),

    }
    serializers = {
        'default': CommerceDetailSerializer,
        'list': CommerceSerializer,
        'create': CommerceCreateSerializer,
        'update': CommerceCreateSerializer,
        'partial_update': CommerceCreateSerializer,
    }


class MarcheViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = Marche.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': MarcheDetailSerializer,
        'list': MarcheDetailSerializer,
    }


class MarcheHoraireViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = MarcheHoraire.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': MarcheHoraireSerializer
    }


class AssociationViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = Association.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),
        'create': (UserIsPresidentOrSecretaryOrAdmin,),
        'update': (UserIsPresidentOrSecretaryOrAdmin,),
        'partial_update': (UserIsPresidentOrSecretaryOrAdmin,),
        'destroy': (UserIsPresidentOrSecretaryOrAdmin,),

    }
    serializers = {
        'default': AssociationDetailSerializer,
        'list': AssociationSerializer,
        'create': AssociationCreateSerializer,
        'update': AssociationCreateSerializer,
        'partial_update': AssociationCreateSerializer,
    }


class EvenementViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = Evenement.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),
        'create': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'update': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'partial_update': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'destroy': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),

    }
    serializers = {
        'default': EvenementDetailSerializer,
        'list': EvenementSerializer,
        'create': EvenementCreateSerializer,
        'update': EvenementCreateSerializer,
        'partial_update': EvenementCreateSerializer,
    }


class PatrimoineViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = Evenement.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': PatrimoineCreateSerializer,
        'list': PatrimoineSerializer,
        'retrieve': PatrimoineDetailSerializer
    }


class TravailViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = Travail.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': TravailSerializer,
    }


class TerrainViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = Terrain.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': TerrainSerializer,
    }


class DistinctionViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = Distinction.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': DistinctionDetailSerializer,
        'list': DistinctionSerializer,
    }


class NewpaperViewset(MultiSerializerViewSet, ListRetrieveViewSet):
    queryset = Newpaper.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),
        'create': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'update': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'partial_update': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),
        'destroy': (UserIsPresidentOrSecretaryOfAssocOrAdmin,),

    }
    serializers = {
        'default': NewpaperDetailSerializer,
        'list': NewpaperSerializer,
        'create': NewpaperCreateSerializer,
        'update': NewpaperCreateSerializer,
        'partial_update': NewpaperCreateSerializer,
    }

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        number = self.request.query_params.get("number", None)
        is_hall = self.request.query_params.get('is_hall', None)
        owner = self.request.query_params.get('owner', None)
        first_date: str = self.request.query_params.get('first_date', None)
        last_date: str = self.request.query_params.get('last_date', None)

        if number:
            number = int(number)
        if is_hall:
            is_hall = is_hall == 'true' or is_hall == 'True'
        if owner:
            owner = int(owner)
        if first_date:
            year, month, day = first_date.split('-')
            first_date: datetime = datetime(int(year), int(month), int(day))
        if last_date:
            year, month, day = last_date.split('-')
            last_date: datetime = datetime(int(year), int(month), int(day))

        if is_hall is not None:
            queryset = queryset.filter(est_mairie=is_hall)
        elif owner is not None:
            queryset = queryset.filter(owner_id=owner)
        if first_date and last_date:
            queryset = queryset.filter(date__range=(first_date, last_date))
        if number:
            if number < 0:
                queryset = queryset.all()
            elif number >= 0:
                queryset = queryset.all()[0:number]

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset
