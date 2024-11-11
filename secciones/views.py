# secciones/views_api.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from estudiantes.models import Estudiante
from .models import Seccion, SeccionEstudiante
from .serializers import SeccionSerializer, SeccionSerializer2, SeccionEstudianteSerializer

from rest_framework.decorators import api_view, schema

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


estudiante_id_param = openapi.Parameter('estudiante_id', openapi.IN_PATH, description="ID del estudiante", type=openapi.TYPE_INTEGER)
seccion_id_param = openapi.Parameter('seccion_id', openapi.IN_PATH, description="ID de la sección", type=openapi.TYPE_INTEGER)


# Crear sección

class CrearSeccionAPI(generics.CreateAPIView):
    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer
    @swagger_auto_schema(request_body=SeccionSerializer)
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

# Listar secciones
@swagger_auto_schema(method='get')
class ListaSeccionesAPI(generics.ListAPIView):
    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer2
    # secciones/views_api.py

@swagger_auto_schema(method='get')
@api_view(['GET'])
def obtener_seccion_api(request, seccion_id):
    # Obtener el objeto Seccion por su ID
    seccion = get_object_or_404(Seccion, id=seccion_id)
    # Serializar la información de la sección
    serializer = SeccionSerializer2(seccion)
    # Retornar la información de la sección
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='put', manual_parameters=[seccion_id_param])
@api_view(['PUT'])
def editar_seccion_api(request, seccion_id):
    # Obtén la sección
    seccion = get_object_or_404(Seccion, id=seccion_id)

    # Solo actualiza los campos de la sección (sin afectar la relación con estudiantes)
    data = {
        'nombre': request.data.get('nombre', seccion.nombre),
        'curso': request.data.get('curso', seccion.curso.id),
        'fecha_inicio': request.data.get('fecha_inicio', seccion.fecha_inicio),
        'fecha_termino': request.data.get('fecha_termino', seccion.fecha_termino),
        'pagado': request.data.get('pagado', seccion.pagado)
    }

    serializer = SeccionSerializer(seccion, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Sección actualizada exitosamente.'}, status=status.HTTP_200_OK)

    return Response({'success': False, 'error': 'Error al actualizar la sección.'}, status=status.HTTP_400_BAD_REQUEST)


# secciones/views_api.py

@swagger_auto_schema(method='delete', manual_parameters=[seccion_id_param])
@api_view(['DELETE'])
def eliminar_seccion_api(request, seccion_id):
    seccion = get_object_or_404(Seccion, id=seccion_id)

    try:
        seccion.delete()
        return Response({'success': True, 'message': 'Sección eliminada exitosamente.'}, status=status.HTTP_200_OK)
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



# Obtener los estudiantes de la sección
@swagger_auto_schema(method='get')
@api_view(['GET'])
def obtener_estudiantes_en_seccion(request, seccion_id):
    # Obtener la sección
    seccion = get_object_or_404(Seccion, id=seccion_id)

    # Obtener los estudiantes de esa sección
    seccion_estudiantes = SeccionEstudiante.objects.filter(seccion=seccion)
    
    # Serializar los estudiantes
    serializer = SeccionEstudianteSerializer(seccion_estudiantes, many=True)
    return Response(serializer.data)






# Agregar un estudiante a la sección
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'estudiante_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del estudiante a agregar')
    }))
@api_view(['POST'])
def agregar_estudiante_a_seccion(request, seccion_id):
    # Obtener la sección
    seccion = get_object_or_404(Seccion, id=seccion_id)
    
    # Obtener el ID del estudiante
    estudiante_id = request.data.get('estudiante_id')
    
    if not estudiante_id:
        return Response({'success': False, 'error': 'No se proporcionó el ID del estudiante.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Obtener al estudiante
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    
    # Crear la relación Sección-Estudiante
    seccion_estudiante, created = SeccionEstudiante.objects.get_or_create(seccion=seccion, estudiante=estudiante)
    
    if created:
        return Response({'success': True, 'estudiante_id': estudiante.id, 'nombre': estudiante.nombre}, status=status.HTTP_201_CREATED)
    else:
        return Response({'success': False, 'error': 'El estudiante ya está inscrito en esta sección.'}, status=status.HTTP_400_BAD_REQUEST)




# Eliminar estudiante de sección
@swagger_auto_schema(method='delete', manual_parameters=[seccion_id_param, estudiante_id_param])
@api_view(['DELETE'])
def eliminar_estudiante_api(request, seccion_id, estudiante_id):
    seccion_estudiante = get_object_or_404(SeccionEstudiante, seccion_id=seccion_id, estudiante_id=estudiante_id)
    seccion_estudiante.delete()
    return Response({'success': True, 'message': 'Estudiante eliminado correctamente de la sección.'}, status=status.HTTP_204_NO_CONTENT)



# secciones/views_api.py

@swagger_auto_schema(method='put', manual_parameters=[seccion_id_param, estudiante_id_param])
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
    
    
@swagger_auto_schema(method='get', manual_parameters=[seccion_id_param, estudiante_id_param]) 
@api_view(['GET'])
def obtener_estudiante_en_seccion2(request, seccion_id, estudiante_id):
    # Obtener la sección y el estudiante dentro de esa sección
    seccion = get_object_or_404(Seccion, id=seccion_id)
    seccion_estudiante = get_object_or_404(SeccionEstudiante, seccion=seccion, estudiante__id=estudiante_id)

    # Retornar la información del estudiante y su nota
    return Response({
        'estudiante': {
            'id': seccion_estudiante.estudiante.id,
            'nombre': seccion_estudiante.estudiante.nombre
        },
        'nota': seccion_estudiante.nota
    })