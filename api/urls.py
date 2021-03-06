"""trans_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from api.viewsets import *

schema_view = get_schema_view(
    openapi.Info(
        title="Trans_website API",
        default_version='v1',
        description="Hello world",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="lelu.awen@hacari.org"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register('uploaded-image', UploadedImageViewset, basename='uploaded-image')
router.register('user', UserViewset)
router.register('commission', CommissionViewset)
router.register('bulletin', BulletinViewset)
router.register('conseil', ConseilViewset)
router.register('service', ServiceViewset)
router.register('salle-de-fete', SalleDeFeteViewset, basename='salle-de-fete')
router.register('hebergement', HebergementViewset)
router.register('cimetiere', CimetiereViewset)
router.register('commerce', CommerceViewset)
router.register('marche', MarcheViewset)
router.register('marche-horaire', MarcheHoraireViewset, basename='marche-horaire')
router.register('association', AssociationViewset)
router.register('evenement', EvenementViewset)
router.register('patrimoine', PatrimoineViewset)
router.register('travail', TravailViewset)
router.register('terrain', TerrainViewset)
router.register('distinction', DistinctionViewset)
router.register('newpaper', NewpaperViewset)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path(r'api-token-auth/', obtain_jwt_token),
    path(r'api-token-refresh/', refresh_jwt_token),
]
urlpatterns += router.urls
print(router.urls)
