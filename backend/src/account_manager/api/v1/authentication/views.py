from .serializers import LamaTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class LamaTokenObtainPairView(TokenObtainPairView):
    serializer_class = LamaTokenObtainPairSerializer
