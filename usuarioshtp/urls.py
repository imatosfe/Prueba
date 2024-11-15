from django.urls import path
from .views import (
    LoginView, LogoutView, 
    UsuarioListCreateView, UsuarioDetailView, CambiarPasswordView, VerifyTokenView
)

urlpatterns = [
    # Login - Autenticar al usuario y obtener un token
    path('login/', LoginView.as_view(), name='login'),
    
    # Logout - Cerrar sesión eliminando el token
    path('logout/', LogoutView.as_view(), name='logout'),

    # Listar y crear usuarios (requiere autenticación)
    path('lista/', UsuarioListCreateView.as_view(), name='usuario-list-create'),

    # Detalles, actualizar o eliminar un usuario específico (requiere autenticación)
    path('/<int:pk>/', UsuarioDetailView.as_view(), name='usuario-detail'),

    # Cambiar la contraseña del usuario (requiere autenticación)
    path('cambiar-contrasena/', CambiarPasswordView.as_view(), name='cambiar-contrasena'),

    path('verify_token/', VerifyTokenView.as_view(), name='verify_token'),
]
