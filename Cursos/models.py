# cursos/models.py
from django.db import models
from estudiantes.models import Estudiante  # Importa desde la app correcta
from profesores.models import Profesor    # Importa desde la app correcta

class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    profesores = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateField()

    def __str__(self):
        return self.nombre
