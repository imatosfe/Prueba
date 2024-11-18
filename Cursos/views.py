# cursos/views.py
from rest_framework import viewsets
from .models import Curso
from .serializers import CursoSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

class CursoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # El usuario debe estar autenticado
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
