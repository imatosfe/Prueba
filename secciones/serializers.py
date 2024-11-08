# secciones/serializers.py
from rest_framework import serializers
from .models import Seccion, SeccionEstudiante
from estudiantes.models import Estudiante
from Cursos.models import Curso  # Asumo que tienes un modelo de curso

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ['id', 'nombre']  # Ajusta según lo que necesites

class SeccionEstudianteSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer()  # Incluir los detalles del estudiante
    # Puedes incluir otros campos relacionados, como 'nota'
    class Meta:
        model = SeccionEstudiante
        fields = ['estudiante', 'nota']  # Incluye 'nota' si es necesario

class SeccionSerializer(serializers.ModelSerializer):
    estudiantes = SeccionEstudianteSerializer(source='seccionestudiante_set', many=True)  # Obtener la lista de estudiantes y sus notas

    class Meta:
        model = Seccion
        fields = ['id', 'nombre', 'fecha_inicio', 'fecha_termino', 'pagado', 'curso', 'estudiantes']
