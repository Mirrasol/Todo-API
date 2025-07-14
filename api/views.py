from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from api.models import Task
from api.permissions import IsCreatorOrExecutor
from api.serializers import TaskSerializer, UserSerializer


class UserCreateView(generics.CreateAPIView):
    """
    A view to register a new user.
    """
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    A view to work with new and existing tasks, depending on the 
    provided permissions. Authenticated users only.
    Create: all authenticated users.
    Read/update: creator or executor of the task.
    Delete: creator only.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrExecutor]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
    def perform_update(self, serializer):
        task = self.get_object()
        if self.request.user == task.creator:
            serializer.save()
        elif self.request.user == task.executor:
            name = self.request.data.get('name')
            description = self.request.data.get('description')
            if name:
                task.name = name
            if description:
                task.description = description
            task.save()
