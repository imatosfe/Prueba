# estudiantes/views.py
from rest_framework import viewsets
from .models import Estudiante
from .serializers import EstudianteSerializer
from rest_framework.permissions import IsAuthenticated

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    permission_classes = [IsAuthenticated]

