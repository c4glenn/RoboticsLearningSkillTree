from django.urls import path
from .views import RegisterView, UserDetailView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', UserDetailView.as_view(), name='user-detail'), 
    path('logout/', LogoutView.as_view(), name='logout'),
]
