from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from treatments.models import Treatment


class TreatmentTests(APITestCase):

    def setUp(self):
        self.manager_user = User.objects.create_user(username="manager", password="managerpass",
                                                     is_superuser=True, full_name='Manager User')

        self.normal_user = User.objects.create_user(username="normal", password="normalpass", full_name='Normal User')

        self.client.force_authenticate(user=self.manager_user)

    def test_create_treatment(self):
        url = reverse('treatment-create')
        data = {
            "name": "Treatment One",
            "description": "This is a test treatment."
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Treatment.objects.count(), 1)
        self.assertEqual(Treatment.objects.get().name, "Treatment One")

    def test_create_treatment_without_permissions(self):
        url = reverse('treatment-create')
        self.client.force_authenticate(user=self.normal_user)
        data = {
            "name": "Treatment One",
            "description": "This is a test treatment."
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_treatment_profile(self):
        treatment = Treatment.objects.create(name="Treatment One", description="This is a test treatment.")
        url = reverse('treatment-detail', kwargs={'pk': treatment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], treatment.name)

    def test_get_treatment_profile_without_permissions(self):
        treatment = Treatment.objects.create(name="Treatment One", description="This is a test treatment.")
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('treatment-detail', kwargs={'pk': treatment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_treatment(self):
        treatment = Treatment.objects.create(name="Treatment One", description="This is a test treatment.")
        url = reverse('treatment-detail', kwargs={'pk': treatment.pk})
        data = {
            "name": "Updated Treatment",
            "description": "This is an updated test treatment."
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        treatment.refresh_from_db()
        self.assertEqual(treatment.name, "Updated Treatment")
        self.assertEqual(treatment.description, "This is an updated test treatment.")

    def test_update_treatment_without_permissions(self):
        treatment = Treatment.objects.create(name="Treatment One", description="This is a test treatment.")
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('treatment-detail', kwargs={'pk': treatment.pk})
        data = {
            "name": "Updated Treatment",
            "description": "This is an updated test treatment."
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_treatment(self):
        treatment = Treatment.objects.create(name="Treatment One", description="This is a test treatment.")
        url = reverse('treatment-detail', kwargs={'pk': treatment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Treatment.objects.count(), 0)

    def test_delete_treatment_without_permissions(self):
        treatment = Treatment.objects.create(name="Treatment One", description="This is a test treatment.")
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('treatment-detail', kwargs={'pk': treatment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_treatments(self):
        Treatment.objects.create(name="Treatment One", description="This is a test treatment.")
        Treatment.objects.create(name="Treatment Two", description="This is another test treatment.")
        url = reverse('treatment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_treatments_without_permissions(self):
        Treatment.objects.create(name="Treatment One", description="This is a test treatment.")
        Treatment.objects.create(name="Treatment Two", description="This is another test treatment.")
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('treatment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)