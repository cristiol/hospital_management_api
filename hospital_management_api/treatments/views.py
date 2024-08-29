from rest_framework import generics

from treatments.models import Treatment
from treatments.serializers import TreatmentSerializer
from users.permissions import IsGeneralManager


class TreatmentListView(generics.ListAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    permission_classes = [IsGeneralManager]


class TreatmentsRegistrationView(generics.CreateAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    permission_classes = [IsGeneralManager]
