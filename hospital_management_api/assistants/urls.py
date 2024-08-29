from django.urls import path

from assistants.views import AssistantRegistrationView, AssistantListView, AssistantDetailView

urlpatterns = [
    path('', AssistantListView.as_view(), name='assistant-list'),
    path('create/', AssistantRegistrationView.as_view(), name='assistant-create'),
    path('<int:pk>/', AssistantDetailView.as_view(), name='assistant-detail'),

]
