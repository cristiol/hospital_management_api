from patients.serializers import PatientSerializer
from users.permissions import IsGeneralManager
from .models import Patient
from rest_framework import generics


class PatientRegistrationView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsGeneralManager]


class PatientListView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsGeneralManager]
