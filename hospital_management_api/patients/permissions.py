from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from patients.models import Patient


class IsPatient(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='patient').exists())


class IsPatientOfAppointment(BasePermission):
    def has_object_permission(self, request, view, obj):
        patient_user_id = request.user.pk
        patient = get_object_or_404(Patient, user_id=patient_user_id)

        if request.user.is_authenticated:
            return patient == obj.patient