# facturacion/serializers.py

from rest_framework import serializers
from .models import Tarifa, CuentaPorCobrar, Factura

class TarifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarifa
        fields = '__all__'


class CuentaPorCobrarSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source='estudiante.nombre')
    seccion_nombre = serializers.CharField(source='seccion.nombre')
    facturas = serializers.SerializerMethodField()

    class Meta:
        model = CuentaPorCobrar
        fields = ['id', 'estudiante_nombre', 'seccion_nombre', 'monto', 'fecha_factura', 'estado', 'facturas']

    def get_facturas(self, obj):
        # Retornar una lista de facturas asociadas a la cuenta
        facturas = obj.facturas.all()  # Obtenemos todas las facturas asociadas
        return [{"id": factura.id, "numero_factura": factura.numero_factura, "total": factura.total} for factura in facturas]
# facturacion/serializers.py
from .models import Factura

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['numero_factura', 'estudiante', 'total', 'pagado', 'mes_correspondiente', 'fecha_emision']
