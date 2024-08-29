from django.urls import path

from assistants.views import AssistantRegistrationView

urlpatterns = [
    path('create/', AssistantRegistrationView.as_view(), name='assistant-create'),
]
