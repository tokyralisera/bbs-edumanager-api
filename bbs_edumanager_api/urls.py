from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuration Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="BBS EduManager API",
        default_version='v1',
        description="API de gestion académique pour Bank and Business School",
        terms_of_service="https://www.bbs.edu/terms/",
        contact=openapi.Contact(email="contact@bbs.edu"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    
    #! Admin
    path('admin/', admin.site.urls),
    
    #! API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-schema/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    #! API Endpoints
    path('api/auth/', include('authentication.urls')),
    path('api/users/', include('users.urls')),
]

# Servir les fichiers statiques et médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "BBS EduManager Administration"
admin.site.site_title = "BBS EduManager"
admin.site.index_title = "Gestion de l'école"