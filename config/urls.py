from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='Dashboard Memo API',
        default_version='v1',
        description='API documentation for dashboard memo',
        contact=openapi.Contact(email='umidgaybullayev955@gmail.com'),
        license=openapi.License(name='Webbro License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("base.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema json'),
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

