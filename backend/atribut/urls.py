from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SekolahViewSet,
    JenjangViewSet,
    KelasViewSet,
    MataPelajaranViewSet
)

router = DefaultRouter()
router.register(r'sekolah', SekolahViewSet)
router.register(r'jenjang', JenjangViewSet)
router.register(r'kelas', KelasViewSet)
router.register(r'mata-pelajaran', MataPelajaranViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 
