from users.permissions import IsGeneralManager
from .models import Assistant
from rest_framework import generics
from .serializers import AssistantSerializer


class AssistantRegistrationView(generics.CreateAPIView):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [IsGeneralManager]
