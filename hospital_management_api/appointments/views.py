from rest_framework import generics
from django_filters import rest_framework as filters

from patients.permissions import IsPatientOfAppointment, IsPatient
from .tasks import send_confirmation_mail
from appointments.models import Slot, Appointment
from appointments.serializers import SlotSerializer, AppointmentSerializer


class SlotFilter(filters.FilterSet):
    start_time__date = filters.DateFilter(field_name='start_time', lookup_expr='date')
    start_time__gte = filters.DateTimeFilter(field_name='start_time', lookup_expr='gte')
    start_time__lte = filters.DateTimeFilter(field_name='start_time', lookup_expr='lte')

    class Meta:
        model = Slot
        fields = ['doctor', 'start_time__date', 'start_time__gte', 'start_time__lte', 'is_booked']


class SlotListView(generics.ListAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SlotFilter


class AppointmentListView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsPatientOfAppointment]
    lookup_field = 'pk'


class AppointmentRegistrationView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsPatient]

    def perform_create(self, serializer):
        serializer.save()
        send_confirmation_mail.delay(serializer.data)




