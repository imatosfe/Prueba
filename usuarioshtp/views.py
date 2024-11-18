
# views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from .models import Usuariohtp
from .serializers import UsuarioSerializer, CambiarContrasenaSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed



class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuariohtp.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

class UsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuariohtp.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

class CambiarPasswordView(generics.UpdateAPIView):
    serializer_class = CambiarContrasenaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if user.check_password(serializer.validated_data['old_password']):
            user.set_password(serializer.validated_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)  # Mantiene la sesión
            return Response({"detail": "Contraseña cambiada con éxito."}, status=status.HTTP_200_OK)
        else:
            return Response({"old_password": ["La contraseña actual es incorrecta."]}, status=status.HTTP_400_BAD_REQUEST)


import json

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            # Verificamos si la solicitud tiene el contenido correcto y tratamos de parsear JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)  # Forzamos el parseo a JSON
            else:
                return Response(
                    {"detail": "El tipo de contenido debe ser application/json."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return Response(
                    {"detail": "El nombre de usuario y la contraseña son requeridos."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Intentamos autenticar al usuario
            user = authenticate(username=username, password=password)

            if user is None:
                return Response(
                    {"detail": "Credenciales incorrectas."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Eliminar cualquier token anterior y generar uno nuevo
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)

            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'nombre': user.nombre,
                'apellido': user.apellido,
                'usuario_activo': user.usuario_activo,
                'usuario_administrador': user.usuario_administrador
            }, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response({"detail": "Error al procesar el JSON."}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # El usuario debe estar autenticado

    def post(self, request, *args, **kwargs):
        try:
            # Obtener el token de la solicitud (token enviado por el cliente)
            token = Token.objects.get(user=request.user)
            token.delete()  # Eliminar el token del usuario
            return Response({"detail": "Sesión cerrada exitosamente."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "No se encontró el token de sesión."}, status=status.HTTP_400_BAD_REQUEST)
        



class VerifyTokenView(APIView):
    authentication_classes = [TokenAuthentication]  # Usamos TokenAuthentication
    permission_classes = []  # No necesitamos permisos ya que la autenticación del token es suficiente

    def post(self, request, *args, **kwargs):
        # Verifica si el token es válido
        user = request.user  # Si el token es válido, el usuario será autenticado automáticamente

        if user.is_authenticated:
            return Response({"is_authenticated": True}, status=200)
        else:
            raise AuthenticationFailed("Token no válido o expirado.")


class PaginaPrincipalView(APIView):
    authentication_classes = [TokenAuthentication]  # Verifica el token usando Django Rest Framework
    permission_classes = [IsAuthenticated]  # Asegura que solo los usuarios autenticados puedan acceder


    def get(self, request, *args, **kwargs):
        # Obtener los detalles del usuario autenticado
        user = request.user

        # Responder con los datos del usuario en formato JSON
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'nombre': user.nombre,
            'apellido': user.apellido,
            'usuario_activo': user.usuario_activo,
            'usuario_administrador': user.usuario_administrador,
        }, status=status.HTTP_200_OK)       