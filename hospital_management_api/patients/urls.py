from django.urls import path

from .serializers import UpdateAppliedTreatmentSerializer
from .views import PatientRegistrationView, PatientListView, PatientDetailView, UpdateAssignedAssistantsView, \
    UpdateRecommendedTreatmentView, UpdateAppliedTreatmentView

urlpatterns = [
    path('', PatientListView.as_view(), name='patients-list'),
    path('create/', PatientRegistrationView.as_view(), name='patient-create'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),

    path('<int:pk>/update-assistants/', UpdateAssignedAssistantsView.as_view(), name='patient-update-assistants'),
    path('<int:pk>/update-applied-treatment/', UpdateAppliedTreatmentView.as_view(), name='patient-update-applied-treatment'),
    path('<int:pk>/update-recommended-treatment/', UpdateRecommendedTreatmentView.as_view(), name='patient-update-recommended-treatment'),
]
