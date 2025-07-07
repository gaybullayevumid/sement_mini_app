from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 
            'telegram_id', 
            'username', 
            'first_name', 
            'last_name', 
            'phone_number', 
            'user_type', 
            'user_type_display',
            'is_active', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_telegram_id(self, value):
        if self.instance and self.instance.telegram_id != value:
            if User.objects.filter(telegram_id=value).exists():
                raise serializers.ValidationError("Bu telegram ID allaqachon mavjud.")
        return value