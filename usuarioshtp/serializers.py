# serializers.py

from rest_framework import serializers
from .models import Usuariohtp

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuariohtp
        fields = ['id', 'email', 'username', 'nombre', 'apellido', 'telefono', 'direccion', 'imagen', 'usuario_activo', 'usuario_administrador']

class CambiarContrasenaSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError("Las nuevas contraseñas no coinciden.")
        return attrs
