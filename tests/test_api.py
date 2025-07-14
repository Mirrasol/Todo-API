from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Task


class UserTestCase(APITestCase):
    fixtures = ['tasks.json','users.json']

    def setUp(self):
        self.client = APIClient()
        self.user1 = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=2)
        self.user3 = get_user_model().objects.get(pk=3)
    
    def test_create_user_successfuly(self):
        self.client.logout()

        new_user = {
            "username": "Devonian",
            "password": "50505",
        }
        url = '/api/create-user/'
        response = self.client.post(url, format='json', data=new_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_user_unsuccessfully(self):
        self.client.logout()

        new_user = {
            "username": "Cambrian",
            "password": "50505",
        }
        url = '/api/create-user/'
        response = self.client.post(url, format='json', data=new_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TaskTestCase(APITestCase):
    fixtures = ['tasks.json', 'users.json']

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.get(pk=1)
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)
    
    def test_create_task_unauthenticated(self):
        """
        Ensure unauthenticated user cannot create a new task.
        """
        url = '/api/task/'
        data = {'name': 'Dangerous Task', 'description': 'Loh!', 'executor': 1}
        response = self.client.post(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_task_authenticated(self):
        """
        Ensure authenticated user can create a new task successfully.
        """
        self.client.force_login(self.user)

        url = f'/api/task/'
        data = {'name': 'Some Task', 'description': 'Loh!', 'executor': 1}
        response = self.client.post(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.get(pk=4).name, 'Some Task')
