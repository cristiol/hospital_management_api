from .views import DoctorPatientReportView, PatientTreatmentReportView
from django.urls import path


urlpatterns = [
    path('doctor-patient-report/', DoctorPatientReportView.as_view(), name='doctor-patient-report'),
    path('<int:pk>/patient-treatment-report/', PatientTreatmentReportView.as_view(), name='patient-treatment-report')
]