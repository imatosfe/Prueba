# secciones/serializers.py
from rest_framework import serializers
from .models import Seccion, SeccionEstudiante
from estudiantes.models import Estudiante

class SeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seccion
        fields = '__all__'  # Ajusta los campos según sea necesario

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ['id', 'nombre']  # Ajusta los campos según sea necesario

class SeccionEstudianteSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer()

    class Meta:
        model = SeccionEstudiante
        fields = ['estudiante', 'nota']  # Ajusta los campos según sea necesario
