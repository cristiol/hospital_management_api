from assistants.permissions import IsAssignedAssistant
from doctors.permissions import IsAssignedDoctor
from patients.serializers import PatientSerializer, UpdateUpdateAssignedAssistantsSerializer, \
    UpdateAppliedTreatmentSerializer, UpdateRecommendedTreatmentSerializer
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


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsGeneralManager]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        serializer = self.get_serializer(instance)
        serializer.delete(instance)


class UpdateAssignedAssistantsView(generics.UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = UpdateUpdateAssignedAssistantsSerializer
    permission_classes = [IsAssignedDoctor]
    lookup_field = 'pk'


class UpdateRecommendedTreatmentView(generics.UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = UpdateRecommendedTreatmentSerializer
    permission_classes = [IsAssignedDoctor]
    lookup_field = 'pk'


class UpdateAppliedTreatmentView(generics.UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = UpdateAppliedTreatmentSerializer
    permission_classes = [IsAssignedAssistant]
    lookup_field = 'pk'




