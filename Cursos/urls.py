# cursos/urls.py
from rest_framework.routers import DefaultRouter
from .views import CursoViewSet

router = DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='curso')  # Registro del ViewSet

urlpatterns = router.urls
