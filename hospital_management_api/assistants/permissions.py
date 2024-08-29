
from rest_framework.permissions import BasePermission
from rest_framework.generics import get_object_or_404
from .models import Assistant


class IsAssistant(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='assistant').exists())


class IsAssignedAssistant(BasePermission):

    def has_object_permission(self, request, view, obj):
        assistant_user_id = request.user.pk
        assistant = get_object_or_404(Assistant, user_id=assistant_user_id)

        if request.user.is_authenticated:
            return assistant in obj.assistants.all()

        return False
