# facturacion/models.py
from estudiantes.models import Estudiante
from secciones.models import Seccion  # Asegúrate de que esta importación sea correcta
from django.db import models, transaction

class Tarifa(models.Model):
    secciones_tarifa = models.OneToOneField(Seccion, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"Tarifa para {self.seccion}: {self.precio}"

class CuentaPorCobrar(models.Model):
    estudiante = models.ForeignKey('estudiantes.Estudiante', on_delete=models.CASCADE)  # Referencia en cadena
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_factura = models.DateField()  # Agrega este campo
    mes_correspondiente = models.CharField(max_length=20)  # Agrega el campo para el mes correspondiente
    
    estado = models.CharField(
        max_length=20,
        choices=[('pendiente', 'Pendiente'), ('pagado', 'Pagado')],
        default='pendiente'
    )

    def __str__(self):
        return f"{self.estudiante} - {self.seccion} - {self.monto} - {self.estado}  - {self.mes_correspondiente}"

    def esta_pendiente(self):
        return self.estado == 'pendiente'

class Factura(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, null=True)  # Cambia a null=True
    cuenta_por_cobrar = models.ForeignKey(CuentaPorCobrar, on_delete=models.CASCADE, related_name='facturas', null=True, blank=True)
   
    numero_factura = models.IntegerField(unique=True, editable=False)
    fecha_emision = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)
    mes_correspondiente = models.CharField(max_length=20)
    # El resto de tu código permanece igual


    def __str__(self):
        return f"Factura {self.numero_factura} - Estudiante: {self.estudiante} - Total: {self.total} - Mes: {self.mes_correspondiente}"

    
    def save(self, *args, **kwargs):
        # Verificar si la factura tiene una cuenta por cobrar asociada
        if self.cuenta_por_cobrar is None:
            raise ValueError("La factura debe tener una cuenta por cobrar asociada.")

        # Asignar un número de factura si no tiene uno
        if not self.numero_factura:
            with transaction.atomic():
                last_invoice = Factura.objects.order_by('numero_factura').last()
                self.numero_factura = (last_invoice.numero_factura + 1) if last_invoice else 1

        # Guardar la factura
        super().save(*args, **kwargs)


