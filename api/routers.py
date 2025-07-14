from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TaskViewSet, UserCreateView

router = DefaultRouter()
router.register(r'task', TaskViewSet)

urlpatterns = [
    path('create-user/', UserCreateView.as_view()),
    path('', include(router.urls)),
]
