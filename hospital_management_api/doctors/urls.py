from django.urls import path
from doctors.views import DoctorDetailView, DoctorRegistrationView, DoctorListView

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('create/', DoctorRegistrationView.as_view(), name='doctor-create'),
    path('<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),

]
