from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import RegistrationUserSerializer


class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationUserSerializer
    permission_classes = [AllowAny]
