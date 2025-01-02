from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import buku as Buku
from .serializers import BukuSerializer, BulkDeleteSerializer, PerangkatKurikulumSerializer, MateriSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import logging
from django.http import HttpResponse, FileResponse
from pdf2image import convert_from_path
import os
from io import BytesIO
from PIL import Image
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.views import APIView
from .models import buku, perangkat_kurikulum, materi
from .serializers import PerangkatKurikulumSerializer, MateriSerializer
from django.http import HttpResponse
from users.models import guru
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from users.models import siswa

class BukuViewSet(viewsets.ModelViewSet):
    queryset = buku.objects.all()
    serializer_class = BukuSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get_queryset(self):
        return self.queryset.select_related(
            'kelas',
            'jenjang',
            'mata_pelajaran',
            'sekolah'
        )
    
    def create(self, request, *args, **kwargs):
        try:
            # Jika sekolah tidak ada di request.data, set None
            mutable_data = request.data.copy()
            if 'sekolah' not in request.data or request.data['sekolah'] == '':
                mutable_data['sekolah'] = None
            
            serializer = self.get_serializer(data=mutable_data)
            if not serializer.is_valid():
                print("Validation errors:", serializer.errors)
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            self.perform_create(serializer)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            print(f"Error creating buku: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def update(self, request, *args, **kwargs):
        # Jika sekolah tidak ada di request.data atau kosong, set None
        if 'sekolah' not in request.data or request.data['sekolah'] == '':
            mutable_data = request.data.copy()
            mutable_data['sekolah'] = None
            
            # Gunakan mutable_data untuk serializer, bukan mengubah request.data
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=mutable_data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return Response(serializer.data)
            
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        try:
            serializer = BulkDeleteSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            ids = serializer.validated_data['ids']
            bukus = self.queryset.filter(id__in=ids)
            
            # Hapus file fisik
            for buku_obj in bukus:
                if buku_obj.file_buku:
                    try:
                        if os.path.exists(buku_obj.file_buku.path):
                            os.remove(buku_obj.file_buku.path)
                    except Exception as e:
                        print(f"Error menghapus file: {str(e)}")
            
            # Hapus record database
            bukus.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='by_guru')
    def by_guru(self, request):
        try:
            user = request.user
            if user.role != 'guru':
                return Response(
                    {'error': 'Hanya guru yang dapat mengakses endpoint ini'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Dapatkan data guru menggunakan model guru
            from users.models import guru
            guru_data = guru.objects.get(user=user)
            if not guru_data:
                return Response(
                    {'error': 'Profil guru tidak ditemukan'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Filter buku berdasarkan sekolah dan mata pelajaran guru
            queryset = self.queryset.filter(
                sekolah=guru_data.sekolah,
                mata_pelajaran=guru_data.nama_mata_pelajaran
            )

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except guru.DoesNotExist:
            return Response(
                {'error': 'Profil guru tidak ditemukan'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='public', permission_classes=[])
    def public_books(self, request):
        try:
            # Ambil buku dengan sekolah=None (buku umum)
            queryset = self.queryset.filter(sekolah__isnull=True)
            
            # Urutkan berdasarkan id terbaru
            queryset = queryset.order_by('-id')
            
            # Batasi jumlah buku yang ditampilkan (opsional)
            limit = request.query_params.get('limit', 10)
            try:
                limit = int(limit)
            except ValueError:
                limit = 10
            
            queryset = queryset[:limit]
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='by_siswa')
    def by_siswa(self, request):
        try:
            user = request.user
            if user.role != 'siswa':
                return Response(
                    {'error': 'Hanya siswa yang dapat mengakses endpoint ini'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            siswa_data = siswa.objects.select_related('sekolah', 'kelas', 'jenjang').get(user=user)
            
            # Filter buku berdasarkan:
            # 1. Buku dari sekolah siswa atau buku umum (sekolah=None)
            # 2. Sesuai jenjang dan kelas siswa
            queryset = self.get_queryset().filter(
                (Q(sekolah=siswa_data.sekolah) | Q(sekolah__isnull=True)),
                jenjang=siswa_data.jenjang,
                kelas=siswa_data.kelas
            ).select_related('mata_pelajaran_detail')

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except siswa.DoesNotExist:
            return Response(
                {'error': 'Profil siswa tidak ditemukan'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def get_pdf_cover(request, file_path):
    try:
        # Bersihkan path dari double slashes
        clean_path = os.path.normpath(file_path)
        
        # Path lengkap ke file PDF
        pdf_path = os.path.join(settings.MEDIA_ROOT, clean_path)
        
        if not os.path.exists(pdf_path):
            return HttpResponse(status=404)
            
        # Konversi halaman pertama PDF ke gambar
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        
        # Ambil halaman pertama
        cover = images[0]
        
        # Konversi ke PNG
        img_io = BytesIO()
        cover.save(img_io, 'PNG', quality=85, optimize=True)
        img_io.seek(0)
        
        return HttpResponse(img_io.getvalue(), content_type='image/png')
    except Exception as e:
        print(f"Error converting PDF: {str(e)}")
        return HttpResponse(status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_pdf(request, file_id):
    try:
        buku_obj = Buku.objects.get(id=file_id)
        file_path = buku_obj.file_buku.path
        
        if not os.path.exists(file_path):
            return Response({'error': 'File tidak ditemukan'}, status=404)
            
        with open(file_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{buku_obj.nama_buku}.pdf"'
            return response
    except Buku.DoesNotExist:
        return Response({'error': 'Buku tidak ditemukan'}, status=404)
    except Exception as e:
        
        return Response({'error': str(e)}, status=500)

class PerangkatKurikulumViewSet(viewsets.ModelViewSet):
    queryset = perangkat_kurikulum.objects.all()
    serializer_class = PerangkatKurikulumSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def perform_create(self, serializer):
        serializer.save(guru=self.request.user)
        
    def get_queryset(self):
        user = self.request.user
        if user.role == 'guru':
            return self.queryset.filter(guru=user).select_related(
                'kelas',
                'jenjang', 
                'mata_pelajaran',
                'guru',
                'sekolah'
            )
        return self.queryset.select_related(
            'kelas',
            'jenjang',
            'mata_pelajaran', 
            'guru',
            'sekolah'
        )
    
    def create(self, request, *args, **kwargs):
        try:
            # Jika sekolah tidak ada di request.data, set None
            mutable_data = request.data.copy()
            if 'sekolah' not in request.data or request.data['sekolah'] == '':
                mutable_data['sekolah'] = None
            
            serializer = self.get_serializer(data=mutable_data)
            if not serializer.is_valid():
                print("Validation errors:", serializer.errors)
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            self.perform_create(serializer)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            print(f"Error creating perangkat: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def update(self, request, *args, **kwargs):
        # Jika sekolah tidak ada di request.data atau kosong, set None
        if 'sekolah' not in request.data or request.data['sekolah'] == '':
            mutable_data = request.data.copy()
            mutable_data['sekolah'] = None
            
            # Gunakan mutable_data untuk serializer, bukan mengubah request.data
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=mutable_data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return Response(serializer.data)
            
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        try:
            serializer = BulkDeleteSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            ids = serializer.validated_data['ids']
            perangkats = self.queryset.filter(id__in=ids)
            
            # Hapus file fisik
            for perangkat_obj in perangkats:
                if perangkat_obj.file_perangkat_kurikulum:
                    try:
                        if os.path.exists(perangkat_obj.file_perangkat_kurikulum.path):
                            os.remove(perangkat_obj.file_perangkat_kurikulum.path)
                    except Exception as e:
                        print(f"Error menghapus file: {str(e)}")
            
            # Hapus record database
            perangkats.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def get_perangkat_cover(request, file_path):
    try:
        # Bersihkan path dari double slashes
        clean_path = os.path.normpath(file_path)
        
        # Path lengkap ke file PDF
        pdf_path = os.path.join(settings.MEDIA_ROOT, clean_path)
        
        if not os.path.exists(pdf_path):
            return HttpResponse(status=404)
            
        # Konversi halaman pertama PDF ke gambar
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        
        # Ambil halaman pertama
        cover = images[0]
        
        # Konversi ke PNG
        img_io = BytesIO()
        cover.save(img_io, 'PNG', quality=85, optimize=True)
        img_io.seek(0)
        
        return HttpResponse(img_io.getvalue(), content_type='image/png')
    except Exception as e:
        print(f"Error converting PDF: {str(e)}")
        return HttpResponse(status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_perangkat(request, file_id):
    try:
        perangkat_obj = perangkat_kurikulum.objects.get(id=file_id)
        file_path = perangkat_obj.file_perangkat_kurikulum.path
        
        if not os.path.exists(file_path):
            return Response({'error': 'File tidak ditemukan'}, status=404)
            
        with open(file_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{perangkat_obj.nama_perangkat_kurikulum}.pdf"'
            return response
    except perangkat_kurikulum.DoesNotExist:
        return Response({'error': 'Perangkat tidak ditemukan'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_perangkat(request, file_id):
    try:
        perangkat_obj = perangkat_kurikulum.objects.get(id=file_id)
        file_path = perangkat_obj.file_perangkat_kurikulum.path
        
        if not os.path.exists(file_path):
            return Response({'error': 'File tidak ditemukan'}, status=404)
            
        # Buka file dan baca kontennya
        pdf_file = open(file_path, 'rb')
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{perangkat_obj.nama_perangkat_kurikulum}.pdf"'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Access-Control-Allow-Origin'] = settings.ACCESS_CONTROL_ALLOW_ORIGIN
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
            
    except perangkat_kurikulum.DoesNotExist:
        return Response({'error': 'Perangkat tidak ditemukan'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

class MateriViewSet(viewsets.ModelViewSet):
    queryset = materi.objects.all()
    serializer_class = MateriSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get_queryset(self):
        return self.queryset.select_related(
            'kelas',
            'jenjang',
            'mata_pelajaran',
            'sekolah',
            'guru'
        )
    
    def perform_create(self, serializer):
        serializer.save(guru=self.request.user)
    
    def create(self, request, *args, **kwargs):
        try:
            # Pastikan status selalu ada dan valid
            mutable_data = request.data.copy()
            status_value = mutable_data.get('status', 'aktif')
            if status_value not in ['aktif', 'tidak_aktif']:
                mutable_data['status'] = 'aktif'
            
            serializer = self.get_serializer(data=mutable_data)
            if not serializer.is_valid():
                print("Validation errors:", serializer.errors)
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            self.perform_create(serializer)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(f"Error creating materi: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        try:
            serializer = BulkDeleteSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            ids = serializer.validated_data['ids']
            materis = self.queryset.filter(id__in=ids)
            
            # Hapus file fisik
            for materi_obj in materis:
                if materi_obj.file_materi:
                    try:
                        if os.path.exists(materi_obj.file_materi.path):
                            os.remove(materi_obj.file_materi.path)
                    except Exception as e:
                        print(f"Error menghapus file: {str(e)}")
            
            # Hapus record database
            materis.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='by_siswa')
    def by_siswa(self, request):
        try:
            user = request.user
            if user.role != 'siswa':
                return Response(
                    {'error': 'Hanya siswa yang dapat mengakses endpoint ini'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            siswa_data = siswa.objects.select_related('sekolah', 'kelas', 'jenjang').get(user=user)
            
            # Filter materi berdasarkan:
            # 1. Materi dari sekolah siswa
            # 2. Sesuai jenjang dan kelas siswa
            # 3. Status aktif
            queryset = self.get_queryset().filter(
                sekolah=siswa_data.sekolah,
                jenjang=siswa_data.jenjang,
                kelas=siswa_data.kelas,
                status='aktif'
            ).select_related('mata_pelajaran_detail', 'guru_detail')

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except siswa.DoesNotExist:
            return Response(
                {'error': 'Profil siswa tidak ditemukan'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_materi(request, file_id):
    try:
        materi_obj = materi.objects.get(id=file_id)
        file_path = materi_obj.file_materi.path
        
        if not os.path.exists(file_path):
            return Response({'error': 'File tidak ditemukan'}, status=404)
            
        with open(file_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{materi_obj.nama_materi}.pdf"'
            return response
    except materi.DoesNotExist:
        return Response({'error': 'Materi tidak ditemukan'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_materi(request, file_id):
    try:
        materi_obj = materi.objects.get(id=file_id)
        file_path = materi_obj.file_materi.path
        
        if not os.path.exists(file_path):
            return Response({'error': 'File tidak ditemukan'}, status=404)
            
        # Buka file dan baca kontennya
        pdf_file = open(file_path, 'rb')
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{materi_obj.nama_materi}.pdf"'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Access-Control-Allow-Origin'] = settings.ACCESS_CONTROL_ALLOW_ORIGIN
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
            
    except materi.DoesNotExist:
        return Response({'error': 'Materi tidak ditemukan'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_guru_profile(request):
    try:
        user = request.user
        if user.role != 'guru':
            return Response(
                {'error': 'Hanya guru yang dapat mengakses endpoint ini'},
                status=status.HTTP_403_FORBIDDEN
            )

        guru_data = guru.objects.get(user=user)
        if not guru_data:
            return Response(
                {'error': 'Profil guru tidak ditemukan'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Gunakan GuruSerializer yang sudah ada
        from users.serializers import GuruSerializer
        serializer = GuruSerializer(guru_data)
        return Response(serializer.data)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_statistics(request):
    try:
        # Dapatkan profil guru dari user
        guru_profile = guru.objects.get(user=request.user)
        if not guru_profile:
            return Response(
                {'error': 'Profil guru tidak ditemukan'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get statistics
        buku_count = buku.objects.filter(
            mata_pelajaran=guru_profile.nama_mata_pelajaran,
            kelas__in=guru_profile.kelas.all(),
            jenjang=guru_profile.jenjang,
            sekolah=guru_profile.sekolah
        ).count()
        
        materi_count = materi.objects.filter(
            mata_pelajaran=guru_profile.nama_mata_pelajaran,
            kelas__in=guru_profile.kelas.all(),
            jenjang=guru_profile.jenjang,
            sekolah=guru_profile.sekolah
        ).count()
        
        perangkat_count = perangkat_kurikulum.objects.filter(
            mata_pelajaran=guru_profile.nama_mata_pelajaran,
            kelas__in=guru_profile.kelas.all(),
            jenjang=guru_profile.jenjang,
            sekolah=guru_profile.sekolah
        ).count()
        
        # Get recent items (last 10) with proper serialization
        recent_buku = BukuSerializer(
            buku.objects.filter(
                mata_pelajaran=guru_profile.nama_mata_pelajaran,
                kelas__in=guru_profile.kelas.all(),
                jenjang=guru_profile.jenjang,
                sekolah=guru_profile.sekolah
            ).order_by('-id')[:10],
            many=True
        ).data
        
        recent_materi = MateriSerializer(
            materi.objects.filter(
                mata_pelajaran=guru_profile.nama_mata_pelajaran,
                kelas__in=guru_profile.kelas.all(),
                jenjang=guru_profile.jenjang,
                sekolah=guru_profile.sekolah
            ).order_by('-id')[:10],
            many=True
        ).data
        
        recent_perangkat = PerangkatKurikulumSerializer(
            perangkat_kurikulum.objects.filter(
                mata_pelajaran=guru_profile.nama_mata_pelajaran,
                kelas__in=guru_profile.kelas.all(),
                jenjang=guru_profile.jenjang,
                sekolah=guru_profile.sekolah
            ).order_by('-id')[:10],
            many=True
        ).data
        
        # Calculate trends
        last_month = timezone.now() - timedelta(days=30)
        buku_trend = calculate_trend(buku, guru_profile, last_month)
        materi_trend = calculate_trend(materi, guru_profile, last_month)
        perangkat_trend = calculate_trend(perangkat_kurikulum, guru_profile, last_month)
        
        # Serialize mata pelajaran data
        mata_pelajaran_data = {
            'id': guru_profile.nama_mata_pelajaran.id,
            'nama_mata_pelajaran': guru_profile.nama_mata_pelajaran.nama_mata_pelajaran
        } if guru_profile.nama_mata_pelajaran else None
        
        return Response({
            'statistics': {
                'totalBuku': buku_count,
                'totalMateri': materi_count,
                'totalPerangkat': perangkat_count,
                'bukuTrend': buku_trend,
                'materiTrend': materi_trend,
                'perangkatTrend': perangkat_trend
            },
            'recent_buku': recent_buku,
            'recent_materi': recent_materi,
            'recent_perangkat': recent_perangkat,
            'guru_profile': guru_profile.user.foto_profil.url if guru_profile.user.foto_profil else None,
            'guru_nama': guru_profile.nama_guru,
            'guru_username': guru_profile.user.username,
            'guru_nama_mata_pelajaran': mata_pelajaran_data
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def calculate_trend(model, guru_profile, last_month):
    current_count = model.objects.filter(
        mata_pelajaran=guru_profile.nama_mata_pelajaran,
        kelas__in=guru_profile.kelas.all(),
        jenjang=guru_profile.jenjang,
        sekolah=guru_profile.sekolah
    ).count()
    
    previous_count = model.objects.filter(
        mata_pelajaran=guru_profile.nama_mata_pelajaran,
        kelas__in=guru_profile.kelas.all(),
        jenjang=guru_profile.jenjang,
        sekolah=guru_profile.sekolah
    ).count()
    
    if previous_count == 0:
        return 100 if current_count > 0 else 0
        
    trend = ((current_count - previous_count) / previous_count) * 100
    return round(trend, 1)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_siswa_statistics(request):
    print("Endpoint accessed")
    try:
        user = request.user
        print(f"User role: {user.role}")
        if user.role != 'siswa':
            return Response(
                {'error': 'Hanya siswa yang dapat mengakses endpoint ini'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Dapatkan data siswa
        siswa_data = siswa.objects.select_related('sekolah', 'kelas', 'jenjang').get(user=user)

        # Filter buku berdasarkan kriteria
        buku_list = buku.objects.filter(
            (Q(sekolah=siswa_data.sekolah) | Q(sekolah__isnull=True)),
            jenjang=siswa_data.jenjang,
            kelas=siswa_data.kelas
        ).select_related(
            'mata_pelajaran',
            'kelas',
            'jenjang',
            'sekolah'
        ).order_by('-id')[:10]

        # Filter materi berdasarkan kriteria
        materi_list = materi.objects.filter(
            (Q(sekolah=siswa_data.sekolah) | Q(sekolah__isnull=True)),
            jenjang=siswa_data.jenjang,
            kelas=siswa_data.kelas,
            status='aktif'
        ).select_related(
            'mata_pelajaran',
            'kelas',
            'jenjang',
            'sekolah',
            'guru'
        ).order_by('-id')[:10]

        return Response({
            'buku': BukuSerializer(buku_list, many=True).data,
            'materi': MateriSerializer(materi_list, many=True).data,
            'siswa': {
                'nama_siswa': siswa_data.nama_siswa,
                'kelas': {
                    'id': siswa_data.kelas.id,
                    'nama_kelas': siswa_data.kelas.nama_kelas
                },
                'jenjang': {
                    'id': siswa_data.jenjang.id,
                    'nama_jenjang': siswa_data.jenjang.nama_jenjang
                },
                'sekolah': {
                    'id': siswa_data.sekolah.id,
                    'nama_sekolah': siswa_data.sekolah.nama_sekolah
                } if siswa_data.sekolah else None
            }
        })

    except siswa.DoesNotExist:
        return Response(
            {'error': 'Profil siswa tidak ditemukan'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
