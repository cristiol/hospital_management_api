from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import Group
from users.models import User
from .models import Assistant


class AssistantTests(APITestCase):

    def setUp(self):
        self.manager_user = User.objects.create_user(username="manager", password="managerpass",
                                                     is_superuser=True, full_name='Manager User')

        self.assistant_user = User.objects.create_user(username="assistant", password="assistantpass")
        self.assistant_group = Group.objects.create(name='assistant')
        self.assistant_user.groups.add(self.assistant_group)
        self.assistant_user.save()

        self.normal_user = User.objects.create_user(username="normal", password="normalpass", full_name='Normal User')

        self.client.force_authenticate(user=self.manager_user)

    def test_create_assistant(self):
        url = reverse('assistant-create')
        data = {
            "user": self.assistant_user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assistant.objects.count(), 1)

    def test_create_assistant_without_permissions(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('assistant-create')
        data = {
            "user": self.assistant_user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_assistant_profile(self):
        assistant = Assistant.objects.create(user=self.assistant_user)
        url = reverse('assistant-detail', kwargs={'pk': assistant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_assistant_profile_without_permissions(self):
        assistant = Assistant.objects.create(user=self.assistant_user)
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('assistant-detail', kwargs={'pk': assistant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_assistant(self):
        assistant = Assistant.objects.create(user=self.assistant_user)
        url = reverse('assistant-detail', kwargs={'pk': assistant.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Assistant.objects.count(), 0)

    def test_delete_assistant_without_permissions(self):
        assistant = Assistant.objects.create(user=self.assistant_user)
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('assistant-detail', kwargs={'pk': assistant.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_assistants(self):
        Assistant.objects.create(user=self.assistant_user)
        Assistant.objects.create(user=self.manager_user)
        url = reverse('assistant-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_assistants_without_permissions(self):
        Assistant.objects.create(user=self.assistant_user)
        Assistant.objects.create(user=self.manager_user)
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('assistant-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)