from rest_framework import serializers
from .models import CustomUser, CollectionRequest

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime, timezone

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data['user_id'] = self.user.id
        return data

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'driver', 'address', 'neighborhood', 'age', 'phone']

class CollectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionRequest
        fields = ['id', 'solicitation_time', 'collection_time', 'status']

CustomUser = get_user_model()

class CollectionRequestSerializer(serializers.ModelSerializer):
    requester = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(driver=False))

    class Meta:
        model = CollectionRequest
        fields = ['requester', 'driver', 'solicitation_time', 'collection_time', 'status']

    def create(self, validated_data):
        validated_data['solicitation_time'] = datetime.now()
        validated_data['status'] = 'in_progress'
        
        if 'driver' not in validated_data:
            validated_data['driver'] = None
        
        return super().create(validated_data)

class UnattendedRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    solicitation_time = serializers.DateTimeField()
    address = serializers.CharField(max_length=255)
    neighborhood = serializers.CharField(max_length=255)

class CollectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionRequest
        fields = ['id', 'status', 'collection_time', 'solicitation_time', 'requester', 'driver']

    def update(self, instance, validated_data):
        # Atualiza o status para "completed" e define a hora da coleta
        if validated_data.get('status') == 'completed':
            instance.collection_time = datetime.now()
        instance.status = validated_data.get('status', instance.status)
        
        # Atualiza o driver, se fornecido
        instance.driver = validated_data.get('driver', instance.driver)

        instance.save()
        return instance
