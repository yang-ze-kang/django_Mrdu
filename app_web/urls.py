#!/usr/bin/env python
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from app import views
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

schema_view = get_schema_view(title='API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
                  path('', include(router.urls)),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('admin/', admin.site.urls),
                  path('web/', include('web.urls')),
                  path('app/', include('app.urls')),
                  path('docs/', schema_view, name='docs'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
