# profesores/serializers.py
from rest_framework import serializers
from .models import Profesor  # Asegúrate de importar 'Profesor', no 'profesores'

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'
