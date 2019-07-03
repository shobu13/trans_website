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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

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

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path(r'markdownx/', include('markdownx.urls')),
    path('api/', include('api.urls')),
    path('', lambda request: redirect(to='api/'))
]
try:
    from trans_website.env_settings import local

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(local.MEDIA_URL, document_root=local.MEDIA_ROOT)
except ImportError:
    print("No local config found")
