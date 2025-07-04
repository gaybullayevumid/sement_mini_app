from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views

schema_view = get_schema_view(
    openapi.Info(
        title="Sement Savdo",
        default_version="v1",
        description="API documentation for sement savdo",
        contact=openapi.Contact(email="umidgaybullayev955@gmail.com"),
        license=openapi.License(name="Webbro License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("api/", include("base.urls")),
    path(
        "", schema_view.with_ui("swagger", cache_timeout=0), name="schema json"
    ),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
