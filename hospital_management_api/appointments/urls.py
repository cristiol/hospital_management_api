from django.urls import path
from appointments.views import AppointmentListView, AppointmentsDetailView, AppointmentRegistrationView, SlotListView


urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointments'),
    path('<int:pk>/', AppointmentsDetailView.as_view(), name='appointment-detail'),
    path('create/', AppointmentRegistrationView.as_view(), name='appointment-registration'),

    path('slots/', SlotListView.as_view(), name='slots'),

]