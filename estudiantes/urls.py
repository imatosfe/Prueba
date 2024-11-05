


from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EstudianteViewSet

router = DefaultRouter()
router.register(r'', EstudianteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]   