from users.permissions import IsGeneralManager
from .models import Assistant
from rest_framework import generics
from .serializers import AssistantSerializer


class AssistantRegistrationView(generics.CreateAPIView):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [IsGeneralManager]


class AssistantListView(generics.ListAPIView):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [IsGeneralManager]


class AssistantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [IsGeneralManager]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        serializer = self.get_serializer(instance)
        serializer.delete(instance)


