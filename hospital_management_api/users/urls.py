from .views import UserListView, UserRegistrationView, UserDetailView
from django.urls import path


urlpatterns = [
    path('', UserListView.as_view(), name='get-users'),
    path('create/', UserRegistrationView.as_view(), name='add-user'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail-user'),
]
