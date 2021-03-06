from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from rest_framework import permissions
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import Auth.urls, Lesson.urls, Request.urls

schema_view = get_schema_view(
   openapi.Info(
      title="Music API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('Auth.urls')),
    path('', include('Lesson.urls')),
    path('request/', include('Request.urls')),
    re_path('redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

api_patterns = [
    path('api/auth/', include(Auth.urls.api_patterns)),
    path('api/lesson/', include(Lesson.urls.api_patterns)),
    path('api/request/', include(Request.urls.api_patterns)),
]

urlpatterns += api_patterns

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)