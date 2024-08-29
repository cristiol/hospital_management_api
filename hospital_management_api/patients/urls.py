from django.urls import path

from .views import PatientRegistrationView, PatientListView, PatientDetailView

urlpatterns = [
    path('', PatientListView.as_view(), name='patients-list'),
    path('create/', PatientRegistrationView.as_view(), name='patient-create'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),

]
