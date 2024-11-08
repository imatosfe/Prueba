
from django.urls import path

from .views import (
    CrearSeccionAPI,
    ListaSeccionesAPI,
    editar_seccion_api,
    gestionar_seccion_api,
    editar_estudiante_en_seccion_api,
    eliminar_seccion_api,
    eliminar_estudiante_api,
    obtener_seccion_api,
)



urlpatterns = [
  
    path('', CrearSeccionAPI.as_view(), name='crear_seccion'),
      path('secciones/obt/<int:seccion_id>/', obtener_seccion_api, name='obtener_seccion'),  # GET
  
    path('lista/', ListaSeccionesAPI.as_view(), name='lista_secciones'),
    path('/<int:seccion_id>/', gestionar_seccion_api, name='gestionar_seccion'),
    path('<int:seccion_id>', editar_seccion_api, name='editar_seccion'),
    path('<int:seccion_id>/estudiantes/<int:estudiante_id>/', editar_estudiante_en_seccion_api, name='editar_estudiante_en_seccion'),  # Nueva ruta
    path('eliminar/<int:seccion_id>', eliminar_seccion_api, name='eliminar_seccion'),
    path('<int:seccion_id>/estudiantes/<int:estudiante_id>', eliminar_estudiante_api, name='eliminar_estudiante'),
]
