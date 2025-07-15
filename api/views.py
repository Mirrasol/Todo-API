from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.models import Task
from api.permissions import IsCreator, IsCreatorOrExecutor
from api.serializers import (
    PermissionsSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    UserSerializer,
)


class UserListCreateView(generics.ListCreateAPIView):
    """
    A view to register a new user
    or to get a list of registered users.
    """
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    """
    A view to create a new task
    or to get a list of created tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TaskReadUpdateView(generics.RetrieveUpdateAPIView):
    """
    A view to read or to update a task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrExecutor]


class TaskDeleteView(generics.DestroyAPIView):
    """
    A view to delete a task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated, IsCreator]


class AssignPermissionsView(generics.UpdateAPIView):
    """
    A view to manage permissions to access a task.
    """
    queryset = Task.objects.all()
    serializer_class = PermissionsSerializer
    permission_classes = [IsAuthenticated, IsCreator]
