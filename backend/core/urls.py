"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, login_view, GuruViewSet, SiswaViewSet, dashboard_stats, get_available_users, UserProfileView, get_siswa_by_user
from django.conf import settings
from django.conf.urls.static import static
from atribut.views import (
    MataPelajaranViewSet,
    KelasViewSet, 
    JenjangViewSet,
    SekolahViewSet
)
from apps.views import BukuViewSet, PerangkatKurikulumViewSet, get_pdf_cover, stream_pdf, stream_perangkat, view_perangkat, MateriViewSet, stream_materi, view_materi, get_dashboard_statistics

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'guru', GuruViewSet, basename='guru')
router.register(r'siswa', SiswaViewSet)
router.register(r'mata-pelajaran', MataPelajaranViewSet, basename='mata-pelajaran')
router.register(r'kelas', KelasViewSet, basename='kelas')
router.register(r'jenjang', JenjangViewSet, basename='jenjang')
router.register(r'sekolah', SekolahViewSet, basename='sekolah')
router.register(r'buku', BukuViewSet, basename='buku')
router.register(r'perangkat-kurikulum', PerangkatKurikulumViewSet, basename='perangkat-kurikulum')
router.register(r'materi', MateriViewSet, basename='materi')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login/', login_view),
    
    path('api/dashboard/stats/', dashboard_stats, name='dashboard-stats'),
    path('api/available-users/', get_available_users, name='available-users'),
    path('api/user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/pdf-cover/<path:file_path>', get_pdf_cover, name='pdf_cover'),
    path('api/buku/<int:file_id>/stream/', stream_pdf, name='stream_pdf'),
    path('api/perangkat-kurikulum/<int:file_id>/stream/', stream_perangkat, name='stream_perangkat'),
    path('api/perangkat-kurikulum/<int:file_id>/stream/', stream_perangkat, name='stream_perangkat'),
    path('api/perangkat-kurikulum/<int:file_id>/view/', view_perangkat, name='view_perangkat'),
    path('api/materi/<int:file_id>/stream/', stream_materi, name='stream_materi'),
    path('api/materi/<int:file_id>/view/', view_materi, name='view_materi'),
    path('api/guru/dashboard-statistics/', get_dashboard_statistics, name='dashboard-guru-statistics'),
    path('api/dashboard/guru/dashboard-statistics/', get_dashboard_statistics, name='dashboard-guru-statistics-alt'),
    path('api/siswa/by-user/<int:user_id>/', get_siswa_by_user, name='siswa-by-user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
