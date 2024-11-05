
from django.urls import path
from .views import (
    CrearSeccionAPI,
    ListaSeccionesAPI,
    editar_seccion_api,
    gestionar_seccion_api,
    editar_estudiante_en_seccion_api,
    eliminar_seccion_api,
    eliminar_estudiante_api,
)

urlpatterns = [
    path('secciones/', CrearSeccionAPI.as_view(), name='crear_seccion'),
    path('secciones/lista/', ListaSeccionesAPI.as_view(), name='lista_secciones'),
    path('secciones/<int:seccion_id>/', gestionar_seccion_api, name='gestionar_seccion'),
    path('secciones/<int:seccion_id>/editar/', editar_seccion_api, name='editar_seccion'),
    path('secciones/<int:seccion_id>/estudiantes/<int:estudiante_id>/editar/', editar_estudiante_en_seccion_api, name='editar_estudiante_en_seccion'),  # Nueva ruta
    path('secciones/<int:seccion_id>/eliminar/', eliminar_seccion_api, name='eliminar_seccion'),
    path('secciones/<int:seccion_id>/estudiantes/<int:estudiante_id>/eliminar/', eliminar_estudiante_api, name='eliminar_estudiante'),
]
