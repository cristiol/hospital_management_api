from users.permissions import IsGeneralManager
from .models import Doctor
from rest_framework import generics
from .serializers import DoctorSerializer


class DoctorRegistrationView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsGeneralManager]


class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsGeneralManager]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsGeneralManager]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        serializer = self.get_serializer(instance)
        serializer.delete(instance)


