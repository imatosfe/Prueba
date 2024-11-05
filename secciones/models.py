from django.db import models

# Create your models here.
# secciones/models.py
from django.db import models
from estudiantes.models import Estudiante
from Cursos.models import Curso
from django.utils import timezone



class Seccion(models.Model):
    nombre = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_termino = models.DateField(null=True, blank=True)
    estudiantes = models.ManyToManyField(Estudiante, related_name='secciones')
    pagado = models.BooleanField(default=False)  # Agregar este campo

    def __str__(self):
        return self.nombre

    def puede_agregar_estudiante(self):
        return self.estudiantes.count() < 25

class SeccionEstudiante(models.Model):
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # Campo para la nota
