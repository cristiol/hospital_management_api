from rest_framework.permissions import BasePermission
from rest_framework.generics import get_object_or_404
from .models import Doctor


class IsDoctor(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='doctor').exists())


class IsAssignedDoctor(BasePermission):

    def has_object_permission(self, request, view, obj):
        doctor_user_id = request.user.pk
        doctor = get_object_or_404(Doctor, user_id=doctor_user_id)

        if request.user.is_authenticated:
            return doctor in obj.doctors.all()

        return False
