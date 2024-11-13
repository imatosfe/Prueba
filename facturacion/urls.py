from django.urls import path
from .views import (
    TarifaListCreateAPI,
    TarifaDetailAPI,
    CuentaPorCobrarListAPI,
    generar_cuentas_api,
    pagar_factura_api,
    listar_facturas_api,
    obtener_detalle_factura,
)

urlpatterns = [
    path('tarifas/', TarifaListCreateAPI.as_view(), name='tarifa-list-create'),  # Listar y crear tarifas
    path('tarifas/<int:pk>/', TarifaDetailAPI.as_view(), name='tarifa-detail'),   # Detalle, actualización y eliminación de tarifas
    path('cuentas/', CuentaPorCobrarListAPI.as_view(), name='cuenta-list'),       # Listar cuentas por cobrar
    path('cuentas/generar/', generar_cuentas_api, name='generar-cuentas'),         # Generar cuentas
    path('cuentas/pagar/<int:cuenta_id>/<int:factura_id>/', pagar_factura_api, name='pagar-factura'),  # Pagar factura
    path('facturas/listar/', listar_facturas_api, name='listar-facturas'),        # Listar facturas
    path('factura_detalle/<int:cuenta_id>/<int:factura_id>/', obtener_detalle_factura, name='obtener_detalle_factura'),
  
]
