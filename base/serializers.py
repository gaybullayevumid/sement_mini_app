# serializers.py
from rest_framework import serializers
from .models import TelegramUser

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'username', 'first_name', 'last_name', 
                 'phone_number', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class TelegramUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'username', 'first_name', 'last_name', 'phone_number']
        
    def validate_telegram_id(self, value):
        if TelegramUser.objects.filter(telegram_id=value).exists():
            raise serializers.ValidationError("Bu Telegram ID allaqachon ro'yxatdan o'tgan")
        return value