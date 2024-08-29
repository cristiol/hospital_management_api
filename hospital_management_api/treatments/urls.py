from django.urls import path
from .views import TreatmentListView, TreatmentsRegistrationView, TreatmentsDetailView

urlpatterns = [
    path('', TreatmentListView.as_view(), name='treatment-list'),
    path('create/', TreatmentsRegistrationView.as_view(), name='treatment-create'),
    path('<int:pk>/', TreatmentsDetailView.as_view(), name='treatment-detail'),

]