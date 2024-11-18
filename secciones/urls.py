
from django.urls import path

from .views import (
    CrearSeccionAPI,
    ListaSeccionesAPI,
    agregar_estudiante_a_seccion,
    editar_seccion_api,
    gestionar_seccion_api,
    editar_estudiante_en_seccion_api,
    eliminar_seccion_api,
    eliminar_estudiante_api,
    obtener_estudiantes_en_seccion,
    obtener_seccion_api,
    obtener_estudiante_en_seccion2,
)



urlpatterns = [
  
    path('', CrearSeccionAPI.as_view(), name='crear_seccion'),
      path('secciones/obt/<int:seccion_id>/', obtener_seccion_api, name='obtener_seccion'),  # GET
          path('<int:seccion_id>/estudiantes/', obtener_estudiantes_en_seccion, name='obtener_estudiantes_en_seccion'),  # GET
    path('<int:seccion_id>/estudiantes/agregar/', agregar_estudiante_a_seccion, name='agregar_estudiante_a_seccion'),  # POST

  
    path('lista/', ListaSeccionesAPI.as_view(), name='lista_secciones'),
    path('<int:seccion_id>/', gestionar_seccion_api, name='gestionar_seccion'),
    path('<int:seccion_id>', editar_seccion_api, name='editar_seccion'),
    path('<int:seccion_id>/estudiantes/<int:estudiante_id>/', editar_estudiante_en_seccion_api, name='editar_estudiante_en_seccion'),  # Nueva ruta
    path('eliminar/<int:seccion_id>', eliminar_seccion_api, name='eliminar_seccion'),
    path('<int:seccion_id>/elim_estudiantes/<int:estudiante_id>/', eliminar_estudiante_api, name='eliminar_estudiante'),
    path('secciones/<int:seccion_id>/estudiantes/<int:estudiante_id>/', obtener_estudiante_en_seccion2, name='obtener_estudiante_en_seccion'),
 
]
