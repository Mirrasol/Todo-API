from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken
from api.models import Task


class UserTestCase(APITestCase):
    fixtures = ['tasks.json','users.json']

    def setUp(self):
        self.client = APIClient()
    
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
        self.user1 = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=2)
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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_task_authenticated(self):
        """
        Ensure authenticated user can create a new task successfully.
        """
        access_token = AccessToken.for_user(self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(access_token)
        )

        url = '/api/task/'
        data = {'name': 'Some Task', 'description': 'Loh!', 'executor': 1}
        response = self.client.post(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.get(pk=4).name, 'Some Task')
    
    def test_read_task_unauthorized(self):
        """
        Ensure unauthorized user cannot read the task.
        """
        access_token = AccessToken.for_user(self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(access_token)
        )

        url = '/api/task/2/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_read_task_authorized(self):
        """
        Ensure authorized user can read the task successfully.
        """
        access_token = AccessToken.for_user(self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(access_token)
        )

        url = '/api/task/3/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Project C')
    
    def test_update_task_unauthorized(self):
        """
        Ensure unauthorized user cannot update the task.
        """
        access_token = AccessToken.for_user(self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(access_token)
        )

        url = '/api/task/2/'
        data = {"description": "Times Change"}
        response = self.client.patch(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            Task.objects.get(pk=2).description,
            'Refactoring the existing environment',
        )
        
    def test_update_task_authorized(self):
        """
        Ensure authorized user can update the task successfully.
        """
        access_token = AccessToken.for_user(self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(access_token)
        )

        url = '/api/task/3/'
        data = {"description": "Times Change"}
        response = self.client.patch(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(pk=3).description, 'Times Change')
    
    def test_update_task_permission_unauthorized(self):
        """
        Ensure non-creator cannot assign a new executor to the task.
        """
        access_token = AccessToken.for_user(self.user2)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(access_token)
        )

        url = '/api/task/3/'
        data = {"executor": "1"}
        response = self.client.patch(url, format='json', data=data)
        self.assertEqual(Task.objects.get(pk=3).executor.id, 2)

    def test_update_task_permission_authorized(self):
        """
        Ensure the creator can assign a new executor to the task.
        """
        access_token = AccessToken.for_user(self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(access_token)
        )

        url = '/api/task/3/'
        data = {"description": "Times Change"}
        response = self.client.patch(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(pk=3).description, 'Times Change')
    
    def test_delete_task_unauthorized(self):
        """
        Ensure unauthorized user cannot delete the task.
        """
        access_token = AccessToken.for_user(self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(access_token)
        )

        url = '/api/task/2/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.get(pk=2).name, 'Project B')

    def test_delete_task_authorized(self):
        """
        Ensure authorized user can delete the task successfully.
        """
        access_token = AccessToken.for_user(self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(access_token)
        )

        url = '/api/task/3/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.contains(self.task3))
