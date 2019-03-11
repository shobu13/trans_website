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
        queryset = queryset.filter(groups__name__contains="Élus")

        response['maire'] = self.get_serializer(queryset.filter(elu_role__name='maire'), many=True).data
        response['adjoint1'] = self.get_serializer(queryset.filter(elu_role__name='adjoint1'), many=True).data
        response['adjoint2'] = self.get_serializer(queryset.filter(elu_role__name='adjoint2'), many=True).data
        response['adjoint3'] = self.get_serializer(queryset.filter(elu_role__name='adjoint3'), many=True).data
        response['conseillers'] = self.get_serializer(queryset.filter(elu_role__name='conseiller'), many=True).data
        return Response(response)


class CommissionViewset(MultiSerializerViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                        mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
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


class BulletinViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Bulletin.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': BulletinSerializer,
    }


class ConseilViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Conseil.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': ConseilDetailSerializer,
        'list': ConseilSerializer
    }


class ServiceViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Service.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': ServiceDetailSerializer,
        'list': ServiceSerializer,
    }


class SalleDeFeteViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = SalleDeFete.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': SalleDeFeteDetailSerializer,
        'list': SalleDeFeteSerializer
    }


class HebergementViewset(MultiSerializerViewSet, CrudViewSet):
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


class CimetiereViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Cimetiere.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': CimetiereDetailSerializer,
        'list': CimetiereSerializer,
    }


class CommerceViewset(MultiSerializerViewSet, CrudViewSet):
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


class MarcheViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Marche.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': MarcheDetailSerializer,
        'list': MarcheSerializer,
    }


class MarcheHoraireViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = MarcheHoraire.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': MarcheHoraireSerializer
    }


class AssociationViewset(MultiSerializerViewSet, CrudViewSet):
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


class EvenementViewset(MultiSerializerViewSet, CrudViewSet):
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


class PatrimoineViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Evenement.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': PatrimoineCreateSerializer,
        'list': PatrimoineSerializer,
        'retrieve': PatrimoineDetailSerializer
    }


class TravailViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Travail.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': TravailSerializer,
    }


class TerrainViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Terrain.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': TerrainSerializer,
    }


class DistinctionViewset(MultiSerializerViewSet, CrudViewSet):
    queryset = Distinction.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),

    }
    serializers = {
        'default': DistinctionDetailSerializer,
        'list': DistinctionSerializer,
    }


class NewpaperViewset(MultiSerializerViewSet, CrudViewSet):
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

    # @action(
    #     detail=False,
    #     methods=['get'],
    #     url_path='retrieve-full',
    # )
    # def last_newpaper(self, request, *args, **kwargs):
    #     number = request.query_params.get("number") or 3
    #     is_hall = request.query_params.get('is_hall') or False
    #
    #     if number < 0 or type(is_hall) is not type(bool):
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     queryset = queryset.filter(est_mairie=is_hall)[0:number]
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        number = self.request.query_params.get("number") or None
        is_hall = self.request.query_params.get('is_hall') or None
        owner = self.request.query_params.get('owner') or None
        year = self.request.query_params.get('year') or None
        month = self.request.query_params.get('month') or None

        if number:
            number = int(number)
        if is_hall:
            is_hall = int(is_hall) >= 1
        if owner:
            owner = int(owner)
        if year:
            year = int(year)
        if month:
            month = int(month)

        print(is_hall, number, year)

        if is_hall is not None:
            queryset = queryset.filter(est_mairie=is_hall)
        elif owner is not None:
            queryset = queryset.filter(owner_id=owner)
        if year:
            queryset = queryset.filter(date__year=year)
        if month:
            queryset = queryset.filter(date__month=month)
        if number:
            if number < 0:
                queryset = queryset.all()
            elif number >= 0:
                queryset = queryset.all()[0:number]

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset
