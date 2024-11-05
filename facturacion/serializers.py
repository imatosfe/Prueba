# facturacion/serializers.py

from rest_framework import serializers
from .models import Tarifa, CuentaPorCobrar, Factura

class TarifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarifa
        fields = '__all__'

class CuentaPorCobrarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaPorCobrar
        fields = '__all__'

# facturacion/serializers.py
from .models import Factura

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['numero_factura', 'estudiante', 'total', 'pagado', 'mes_correspondiente', 'fecha_emision']
