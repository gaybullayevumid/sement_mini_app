from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.TelegramUserListView.as_view(), name='user-list'),
    path('users/create/', views.create_user, name='user-create'),
    path('users/<int:telegram_id>/', views.get_user_by_telegram_id, name='user-detail'),
    path('users/<int:telegram_id>/update/', views.update_user_by_telegram_id, name='user-update'),
    path('health/', views.health_check, name='health-check'),  # Qo'shilgan yangi endpoint
]