from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.models import Task


class UserSerializer(serializers.ModelSerializer):
    """
    Custom User serializer.
    """
    id = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'password',
        ]
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Custom Task serializer.
    """
    id = serializers.ReadOnlyField()
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'creator',
            'executor',
        ]
    
    def to_representation(self, instance):
        rep = super(TaskCreateSerializer, self).to_representation(instance)
        rep['creator'] = instance.creator.username
        rep['executor'] = instance.executor.username
        return rep


class TaskUpdateSerializer(serializers.ModelSerializer):
    """
    Custom Task's serializer for updating and reading.
    """
    id = serializers.ReadOnlyField()
    creator = serializers.ReadOnlyField(source='creator.username')
    executor = serializers.ReadOnlyField(source='executor.username')
    
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'description',
            'creator',
            'executor',
        ]


class PermissionsSerializer(serializers.ModelSerializer):
    """
    Custom Task's Permissions serializer.
    """
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'executor',
        ]
    
    def to_representation(self, instance):
        rep = super(PermissionsSerializer, self).to_representation(instance)
        rep['executor'] = instance.executor.username
        return rep
