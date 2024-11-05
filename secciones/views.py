# secciones/views_api.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from estudiantes.models import Estudiante
from .models import Seccion, SeccionEstudiante
from .serializers import SeccionSerializer, SeccionEstudianteSerializer

# Crear sección
class CrearSeccionAPI(generics.CreateAPIView):
    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer

# Listar secciones
class ListaSeccionesAPI(generics.ListAPIView):
    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer
    # secciones/views_api.py

@api_view(['PUT'])
def editar_seccion_api(request, seccion_id):
    seccion = get_object_or_404(Seccion, id=seccion_id)
    serializer = SeccionSerializer(seccion, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Sección actualizada exitosamente.'}, status=status.HTTP_200_OK)

    return Response({'success': False, 'error': 'Error al actualizar la sección.'}, status=status.HTTP_400_BAD_REQUEST)


# secciones/views_api.py

@api_view(['DELETE'])
def eliminar_seccion_api(request, seccion_id):
    seccion = get_object_or_404(Seccion, id=seccion_id)

    try:
        seccion.delete()
        return Response({'success': True, 'message': 'Sección eliminada exitosamente.'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Gestionar sección (listar estudiantes y añadir)
@api_view(['GET', 'POST'])
def gestionar_seccion_api(request, seccion_id):
    seccion = get_object_or_404(Seccion, id=seccion_id)
    
    if request.method == 'POST':
        data = request.data
        estudiante_id = data.get('estudiante_id')
        
        if estudiante_id:
            estudiante = get_object_or_404(Estudiante, id=estudiante_id)
            seccion_estudiante, created = SeccionEstudiante.objects.get_or_create(seccion=seccion, estudiante=estudiante)
            
            if created:
                return Response({'success': True, 'nombre': estudiante.nombre, 'nota': seccion_estudiante.nota, 'estudiante_id': estudiante.id}, status=status.HTTP_201_CREATED)
            else:
                return Response({'success': False, 'error': 'El estudiante ya está en la sección.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': False, 'error': 'No se proporcionó el ID del estudiante.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Para la lista de estudiantes en la sección
    seccion_estudiantes = SeccionEstudiante.objects.filter(seccion=seccion)
    serializer = SeccionEstudianteSerializer(seccion_estudiantes, many=True)
    return Response(serializer.data)



# Eliminar estudiante de sección
@api_view(['DELETE'])
def eliminar_estudiante_api(request, seccion_id, estudiante_id):
    seccion_estudiante = get_object_or_404(SeccionEstudiante, seccion_id=seccion_id, estudiante_id=estudiante_id)
    seccion_estudiante.delete()
    return Response({'success': True, 'message': 'Estudiante eliminado correctamente de la sección.'}, status=status.HTTP_204_NO_CONTENT)



# secciones/views_api.py

@api_view(['PUT'])
def editar_estudiante_en_seccion_api(request, seccion_id, estudiante_id):
    seccion = get_object_or_404(Seccion, id=seccion_id)
    seccion_estudiante = get_object_or_404(SeccionEstudiante, seccion=seccion, estudiante__id=estudiante_id)

    nota = request.data.get('nota')
    if nota is not None:  # Verifica que la nota se haya proporcionado
        try:
            seccion_estudiante.nota = float(nota)  # Cambia esto si esperas otro tipo de datos
            seccion_estudiante.save()
            return Response({'success': True, 'nombre': seccion_estudiante.estudiante.nombre, 'nota': seccion_estudiante.nota}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'success': False, 'error': 'La nota debe ser un número válido.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'success': False, 'error': 'No se proporcionó la nota.'}, status=status.HTTP_400_BAD_REQUEST)
