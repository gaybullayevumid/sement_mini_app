# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('api/users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<str:telegram_id>/', views.UserRetrieveUpdateView.as_view(), name='user-detail'),
    path('api/register/', views.register_user, name='register-user'),
    path('api/user/<str:telegram_id>/', views.get_user_by_telegram_id, name='get-user'),
    path('api/sellers/', views.sellers_list, name='sellers-list'),
    path('api/clients/', views.clients_list, name='clients-list'),
    
    # Mini app
    path('miniapp/', views.miniapp_view, name='miniapp'),
]

# Main project urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]