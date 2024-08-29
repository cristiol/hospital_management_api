from django.urls import path

from assistants.views import AssistantRegistrationView, AssistantListView

urlpatterns = [
    path('', AssistantListView.as_view(), name='assistant-list'),
    path('create/', AssistantRegistrationView.as_view(), name='assistant-create'),
]
