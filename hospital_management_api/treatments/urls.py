from django.urls import path
from .views import TreatmentListView, TreatmentsRegistrationView

urlpatterns = [
    path('', TreatmentListView.as_view(), name='treatment-list'),
    path('create/', TreatmentsRegistrationView.as_view(), name='treatment-create'),

]