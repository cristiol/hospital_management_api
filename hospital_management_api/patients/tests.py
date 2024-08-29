from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import Group
from users.models import User
from doctors.models import Doctor
from assistants.models import Assistant
from treatments.models import Treatment
from patients.models import Patient


class PatientTests(APITestCase):

    def setUp(self):
        self.manager_user = User.objects.create_user(username="manager", password="managerpass", is_superuser=True,
                                                     full_name='Manager User')

        self.doctor_user = User.objects.create_user(username="doctor", password="doctorpass")
        self.doctor_group = Group.objects.create(name='doctors')
        self.doctor_user.groups.add(self.doctor_group)
        self.doctor_user.save()

        self.assistant_user = User.objects.create_user(username="assistant", password="assistantpass")
        self.assistant_group = Group.objects.create(name='assistants')
        self.assistant_user.groups.add(self.assistant_group)
        self.assistant_user.save()

        self.patient_user = User.objects.create_user(username="patient", password="patientpass")
        self.patient_group = Group.objects.create(name='patient')
        self.patient_user.groups.add(self.patient_group)
        self.patient_user.save()

        self.normal_user = User.objects.create_user(username="normal", password="normalpass", full_name='Normal User')

        self.client.force_authenticate(user=self.manager_user)

        self.doctor = Doctor.objects.create(user=self.doctor_user)
        self.assistant = Assistant.objects.create(user=self.assistant_user)
        self.treatment = Treatment.objects.create(name="Treatment One")


    def test_create_patient(self):
        url = reverse('patient-create')
        data = {
            "user": self.patient_user.id,
            "doctors": [self.doctor.id],
            "assistants": [self.assistant.id],
            "recommended_treatment": self.treatment.id,
            "applied_treatment": self.treatment.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)

    def test_create_patient_without_permissions(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('patient-create')
        data = {
            "name": "Patient One",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_patient_profile(self):
        patient = Patient.objects.create(user=self.patient_user)
        url = reverse('patient-detail', kwargs={'pk': patient.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_patient_profile_without_permissions(self):
        patient = Patient.objects.create(user=self.patient_user)
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('patient-detail', kwargs={'pk': patient.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_patient(self):
        patient = Patient.objects.create(user=self.patient_user)
        url = reverse('patient-detail', kwargs={'pk': patient.pk})
        data = {
            "user": self.normal_user.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(patient.user.id, self.normal_user.id)

    def test_update_patient_without_permissions(self):
        patient = Patient.objects.create(user=self.patient_user)
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('patient-detail', kwargs={'pk': patient.pk})
        data = {
            "user": self.normal_user.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_patient(self):
        patient = Patient.objects.create(user=self.patient_user)
        url = reverse('patient-detail', kwargs={'pk': patient.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Patient.objects.count(), 0)

    def test_delete_patient_without_permissions(self):
        patient = Patient.objects.create(user=self.patient_user)
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('patient-detail', kwargs={'pk': patient.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_patients(self):
        Patient.objects.create(user=self.patient_user)
        url = reverse('patients-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_patients_without_permissions(self):
        Patient.objects.create(user=self.patient_user)
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('patients-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_applied_treatment(self):
        patient = Patient.objects.create(user=self.patient_user, applied_treatment=self.treatment)
        patient.assistants.set([self.assistant.id])
        self.client.force_authenticate(user=self.assistant_user)

        url = reverse('patient-update-applied-treatment', kwargs={'pk': patient.pk})
        new_treatment = Treatment.objects.create(name="New Treatment")
        data = {
            "applied_treatment": new_treatment.id
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(patient.applied_treatment, new_treatment)

    def test_update_applied_treatment_without_permissions(self):
        patient = Patient.objects.create(user=self.patient_user, applied_treatment=self.treatment)
        url = reverse('patient-update-applied-treatment', kwargs={'pk': patient.pk})
        new_treatment = Treatment.objects.create(name="New Treatment")
        data = {
            "applied_treatment": new_treatment.id
        }
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_recommended_treatment(self):
        patient = Patient.objects.create(user=self.patient_user, recommended_treatment=self.treatment)
        patient.doctors.set([self.doctor.id])
        self.client.force_authenticate(user=self.doctor_user)

        url = reverse('patient-update-recommended-treatment', kwargs={'pk': patient.pk})
        new_treatment = Treatment.objects.create(name="New Treatment")
        data = {
            "recommended_treatment": new_treatment.id
        }
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(patient.recommended_treatment, new_treatment)

    def test_update_recommended_treatment_without_permissions(self):
        patient = Patient.objects.create(user=self.patient_user, recommended_treatment=self.treatment)
        url = reverse('patient-update-recommended-treatment', kwargs={'pk': patient.pk})
        new_treatment = Treatment.objects.create(name="New Treatment")
        data = {
            "recommended_treatment": new_treatment.id
        }
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_assigned_assistants(self):
        patient = Patient.objects.create(user=self.normal_user)
        patient.doctors.set([self.doctor.id])
        url = reverse('patient-update-assistants', kwargs={'pk': patient.pk})
        data = {
            "assistants": [self.assistant.id]
        }
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(list(patient.assistants.all()), [self.assistant])

    def test_update_assigned_assistants_without_permissions(self):
        patient = Patient.objects.create(user=self.doctor_user)
        url = reverse('patient-update-assistants', kwargs={'pk': patient.pk})
        data = {
            "assistants": [self.assistant.id]
        }
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
