from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from .models import User


class UserTests(APITestCase):
    def setUp(self):
        self.manager_user = User.objects.create_user(username='manager', password='password', is_superuser=True,
                                                     full_name='Manager User')
        self.regular_user = User.objects.create_user(username='regularuser', password='password', full_name='Regular User')

        self.client = APIClient()

    def test_get_users_as_manager(self):
        self.client.force_authenticate(user=self.manager_user)
        url = reverse('get-users')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_users_as_non_manager(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('get-users')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_single_user(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('detail-user', args=[self.regular_user.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.regular_user.username)

    def test_add_user(self):
        url = reverse('add-user')
        data = {
            'username': 'newuser',
            'full_name': 'New User',
            'password': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(username='newuser').full_name, 'New User')

    def test_update_user(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('detail-user', args=[self.regular_user.pk])
        data = {
            'full_name': 'Updated Regular User'
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.full_name, 'Updated Regular User')

    def test_delete_user(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('detail-user', args=[self.regular_user.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_authenticated_user_cannot_access_protected_views(self):
        url = reverse('get-users')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)