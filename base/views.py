from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from typing import Dict, Any
from .models import TelegramUser
from .serializers import TelegramUserSerializer, TelegramUserCreateSerializer


@api_view(['GET'])
def health_check(request) -> JsonResponse:
    """API ishlayotganligini tekshirish"""
    return JsonResponse(
        {"status": "ok", "service": "Telegram User API"},
        status=200
    )


class TelegramUserListView(generics.ListAPIView):
    """Barcha Telegram foydalanuvchilar ro'yxatini olish"""
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    pagination_class = None  # Pagination ishlatilmaydi


class TelegramUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Telegram ID orqali userni olish, yangilash yoki o'chirish"""
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    lookup_field = 'telegram_id'

@api_view(['POST'])
def create_user(request) -> Response:
    """Create or get existing Telegram user"""
    serializer = TelegramUserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        validated_data = serializer.validated_data
        telegram_id = validated_data['telegram_id']  # Will raise KeyError if missing
        
        user, created = TelegramUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults=validated_data
        )
        
        return Response(
            TelegramUserSerializer(user).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
        
    except KeyError:
        return Response(
            {'error': 'telegram_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_user_by_telegram_id(request, telegram_id: str) -> Response:
    """Telegram ID orqali user ma'lumotlarini olish"""
    try:
        user = TelegramUser.objects.get(telegram_id=telegram_id)
        serializer = TelegramUserSerializer(user)
        return Response(serializer.data)
    except TelegramUser.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT', 'PATCH'])
def update_user_by_telegram_id(request, telegram_id: str) -> Response:
    """Telegram ID orqali user ma'lumotlarini yangilash"""
    try:
        user = TelegramUser.objects.get(telegram_id=telegram_id)
        partial = request.method == 'PATCH'
        
        serializer = TelegramUserSerializer(
            user,
            data=request.data,
            partial=partial
        )
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer.save()
        return Response(serializer.data)
        
    except TelegramUser.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )