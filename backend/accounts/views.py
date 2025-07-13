from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """View to handle user registration."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Blacklist the refresh token
            RefreshToken.for_user(request.user).blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)