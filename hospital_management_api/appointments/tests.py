from datetime import datetime, timedelta, time
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from appointments.models import Slot, Appointment
from appointments.serializers import AppointmentSerializer
from doctors.models import Doctor
from patients.models import Patient
from users.models import User
from django.contrib.auth.models import Group



class AppointmentTests(APITestCase):

    def setUp(self):
        self.doctor_user = User.objects.create_user(username="doctor", password="doctorpass")
        self.doctor_group = Group.objects.create(name='doctors')
        self.doctor_user.groups.add(self.doctor_group)
        self.doctor_user.save()

        self.patient_user = User.objects.create_user(username="patient", password="patientpass")
        self.patient_group = Group.objects.create(name='patient')
        self.patient_user.groups.add(self.patient_group)
        self.patient_user.save()

        self.doctor = Doctor.objects.create(user=self.doctor_user)
        self.patient = Patient.objects.create(user=self.patient_user)

        today = datetime.now().date()
        self.start_time = datetime.combine(today, time(12, 0))
        self.end_time = datetime.combine(today, time(17, 0))

        self.slot = Slot.objects.create(
            doctor=self.doctor, start_time=self.start_time, end_time=self.end_time
        )

        self.new_slot = Slot.objects.create(
            doctor=self.doctor, start_time=self.start_time, end_time=self.end_time
        )

        self.client.force_authenticate(user=self.patient_user)

    def test_create_appointment(self):
        url = reverse('appointment-registration')
        data = {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
            "slot": self.slot.id,

        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)

        appointment = Appointment.objects.get()
        self.assertEqual(appointment.patient, self.patient)
        self.assertEqual(appointment.doctor, self.doctor)
        self.assertEqual(appointment.slot, self.slot)

    def test_create_appointment_with_invalid_slot(self):
        url = reverse('appointment-registration')
        data = {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
            "slot": 100,  # Invalid slot ID
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_appointment_with_existing_slot(self):
        # Create an appointment for the same slot
        Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, slot=self.slot
        )
        url = reverse('appointment-registration')
        data = {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
            "slot": self.slot.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_appointments(self):
        Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, slot=self.slot
        )
        url = reverse('appointments')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        appointment = response.data[0]
        self.assertEqual(appointment['patient'], self.patient.id)
        self.assertEqual(appointment['doctor'], self.doctor.id)
        self.assertEqual(appointment['slot'], self.slot.id)

    def test_get_appointment_detail(self):
        appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, slot=self.slot
        )
        url = reverse('appointment-detail', kwargs={'pk': appointment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = AppointmentSerializer(appointment)
        self.assertEqual(response.data, serializer.data)

    def test_update_appointment(self):
        appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, slot=self.slot
        )

        url = reverse('appointment-detail', kwargs={'pk': appointment.pk})
        data = {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
            "slot": self.new_slot.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appointment.refresh_from_db()
        self.assertEqual(appointment.slot, self.new_slot)
