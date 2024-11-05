# facturacion/utils.py

from .models import Factura, CuentaPorCobrar, Tarifa
from estudiantes.models import Estudiante


def generar_factura_y_cuenta_por_cobrar(estudiante_id):
    estudiante = Estudiante.objects.get(id=estudiante_id)
    secciones = estudiante.secciones.all()  # Las secciones a las que está inscrito el estudiante
    total_factura = 0

    # Calcula el total de la factura según las tarifas de las secciones
    for seccion in secciones:
        tarifa = Tarifa.objects.get(secciones_tarifa=seccion)
        total_factura += tarifa.precio

    # Crear la factura
    factura = Factura.objects.create(estudiante=estudiante, total=total_factura)

    # Crear las cuentas por cobrar individuales para cada sección
    for seccion in secciones:
        tarifa = Tarifa.objects.get(secciones_tarifa=seccion)
        CuentaPorCobrar.objects.create(estudiante=estudiante, seccion=seccion, monto=tarifa.precio)

    return factura

