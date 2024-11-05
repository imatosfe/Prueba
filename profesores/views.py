# profesores/views.py
from rest_framework import viewsets
from .models import Profesor
from .serializers import ProfesorSerializer

class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
