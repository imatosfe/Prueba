# profesores/views.py
from rest_framework import viewsets
from .models import Profesor
from .serializers import ProfesorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class ProfesorViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]  # Verifica el token usando Django Rest Framework
    permission_classes = [IsAuthenticated]  # Asegura que solo los usuarios autenticados puedan acceder

    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
