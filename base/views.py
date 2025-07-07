from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import User
from .serializers import UserSerializer
import json

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'telegram_id'

@api_view(['POST'])
def register_user(request):
    """Register new user from Telegram"""
    try:
        data = request.data
        telegram_id = data.get('telegram_id')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        phone_number = data.get('phone_number', '')
        
        # Check if user already exists
        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'username': f"user_{telegram_id}"
            }
        )
        
        if not created:
            # Update existing user
            user.first_name = first_name
            user.last_name = last_name
            if phone_number:
                user.phone_number = phone_number
            user.save()
        
        serializer = UserSerializer(user)
        return Response({
            'success': True,
            'user': serializer.data,
            'created': created
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_by_telegram_id(request, telegram_id):
    """Get user by telegram ID"""
    try:
        user = User.objects.get(telegram_id=telegram_id)
        serializer = UserSerializer(user)
        return Response({
            'success': True,
            'user': serializer.data
        })
    except User.DoesNotExist:
        return Response({
            'success': False,
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@xframe_options_exempt
def miniapp_view(request):
    """Mini app HTML page"""
    return render(request, 'miniapp.html')

@api_view(['GET'])
def sellers_list(request):
    """Get all sellers"""
    sellers = User.objects.filter(user_type='seller')
    serializer = UserSerializer(sellers, many=True)
    return Response({
        'success': True,
        'sellers': serializer.data
    })

@api_view(['GET'])
def clients_list(request):
    """Get all clients"""
    clients = User.objects.filter(user_type='client')
    serializer = UserSerializer(clients, many=True)
    return Response({
        'success': True,
        'clients': serializer.data
    })