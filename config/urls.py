"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from documents.views import DocumentViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='FULLSTACK',
        default_version='v1',
        description='chto=to',
    ),
    public=True
)

router = routers.SimpleRouter()
router.register('documents', DocumentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('school/', include('school.urls')),
    path('account/', include('school.urls')),
    path('documents/export/', include('documents.urls')),
    path('', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)