
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

from rest_framework_simplejwt.tokens import RefreshToken


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




class LoginView(APIView):
    permission_classes = [AllowAny]  # Permite que cualquier usuario acceda

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"detail": "El nombre de usuario y la contraseña son requeridos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Autenticamos al usuario utilizando el modelo personalizado
        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"detail": "Credenciales incorrectas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Eliminar cualquier token anterior del usuario (para evitar múltiples tokens activos)
        Token.objects.filter(user=user).delete()

        # Generar un nuevo token para el usuario
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
    permission_classes = [IsAuthenticated]  # Asegúrate de que el usuario esté autenticado

    def post(self, request, *args, **kwargs):
        return Response({"isValid": True}, status=200)