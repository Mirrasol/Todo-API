from django.urls import path

from api.views import (
    AssignPermissionsView,
    TaskDeleteView,
    TaskListCreateView,
    TaskReadUpdateView,
    UserListCreateView,
)

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='users_list'),
    path('tasks/', TaskListCreateView.as_view(), name='tasks_list'),
    path('tasks/<int:pk>/', TaskReadUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<int:pk>/assign-permissions/', AssignPermissionsView.as_view()),
]
