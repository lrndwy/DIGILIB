from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User, guru as GuruModel, siswa
from .serializers import UserSerializer, GuruSerializer, SiswaSerializer, KelasSerializer
from .permissions import IsAdmin
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import localtime
from .mixins import LogActivityMixin
from .models import guru, siswa
from django.db.models import Q
from atribut.models import kelas
# ... existing code ...

class UserViewSet(LogActivityMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get('role', None)
        if role is not None:
            queryset = queryset.filter(role=role, is_active=True)
        return queryset

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        try:
            ids = request.data.get('ids', [])
            if not ids:
                return Response(
                    {'error': 'Tidak ada ID yang diberikan'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            User.objects.filter(id__in=ids).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active
            }
        })
    else:
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

class GuruViewSet(viewsets.ModelViewSet):
    queryset = guru.objects.all()
    serializer_class = GuruSerializer

    def get_queryset(self):
        queryset = guru.objects.select_related(
            'user',
            'nama_mata_pelajaran',
            'jenjang',
            'sekolah'
        ).prefetch_related('kelas').all()
        
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nama_guru__icontains=search) |
                Q(user__username__icontains=search)
            )
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            
            # Konversi string ke boolean
            data['crud_buku'] = data.get('crud_buku') in [True, 'true', 'True', '1']
            data['crud_materi'] = data.get('crud_materi') in [True, 'true', 'True', '1']
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def available_users(self, request):
        users = User.objects.filter(role='guru').exclude(guru__isnull=False)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        try:
            ids = request.data.get('ids', [])
            if not ids:
                return Response(
                    {'error': 'Tidak ada ID yang diberikan'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            guru.objects.filter(id__in=ids).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['GET'], url_path='kelas-by-jenjang')
    def kelas_by_jenjang(self, request):
        jenjang_id = request.query_params.get('jenjang_id')
        if not jenjang_id:
            return Response({'error': 'jenjang_id is required'}, status=400)
            
        try:
            kelas_list = kelas.objects.filter(jenjang_id=jenjang_id)
            serializer = KelasSerializer(kelas_list, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class SiswaViewSet(LogActivityMixin, viewsets.ModelViewSet):
    queryset = siswa.objects.all()
    serializer_class = SiswaSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.data.get('user'))
            if user.role != 'siswa':
                return Response(
                    {'error': 'User harus memiliki role siswa'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return super().create(request, *args, **kwargs)
        except User.DoesNotExist:
            return Response(
                {'error': 'User tidak ditemukan'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['GET'])
    def dashboard_statistics(self, request):
        try:
            user = request.user
            if user.role != 'siswa':
                return Response(
                    {'error': 'Hanya siswa yang dapat mengakses endpoint ini'},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Dapatkan data siswa
            siswa_data = siswa.objects.get(user=user)
            print(f"Siswa nama: {siswa_data.nama_siswa}")
            print(f"Siswa sekolah: {siswa_data.sekolah}")
            print(f"Siswa kelas: {siswa_data.kelas}")
            print(f"Siswa jenjang: {siswa_data.jenjang}")
            print(f"Siswa user: {siswa_data.user}")

            # Filter buku berdasarkan kriteria
            from apps.models import buku, materi
            from apps.serializers import BukuSerializer, MateriSerializer
            
            buku_list = buku.objects.filter(
                # sekolah__isnull=True,
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
                    'foto_profil_url': user.foto_profil.url if user.foto_profil else None,
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
                        'nama_sekolah': siswa_data.sekolah.nama_sekolah,
                        'logo': siswa_data.sekolah.logo_sekolah.url if siswa_data.sekolah.logo_sekolah else None
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    # Ambil 10 log aktivitas terbaru
    latest_logs = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]
    
    activities = []
    for log in latest_logs:
        action = 'menambahkan' if log.action_flag == ADDITION else 'mengubah' if log.action_flag == CHANGE else 'menghapus'
        message = f"{log.user.username} {action} {log.content_type.model} - {log.object_repr}"
        activities.append({
            'id': log.id,
            'message': message,
            'time': log.action_time.strftime('%d %B %Y %H:%M')
        })

    from apps.serializers import BukuSerializer, SekolahSerializer
    from apps.models import buku
    from atribut.models import sekolah
    # Ambil 5 buku terbaru
    latest_books = buku.objects.select_related(
        'mata_pelajaran',
        'kelas',
        'jenjang',
        'sekolah'
    ).order_by('-id')[:5]

    # Ambil 5 sekolah terbaru dengan logo
    latest_schools = sekolah.objects.order_by('-id')[:5]
    schools_data = []
    
    for school in latest_schools:
        school_data = {
            'id': school.id,
            'nama_sekolah': school.nama_sekolah,
            'logo': school.logo_sekolah.url if school.logo_sekolah else None
        }
        schools_data.append(school_data)

    stats = {
        'total_users': User.objects.count(),
        'total_guru': guru.objects.count(),
        'total_siswa': siswa.objects.count(),
        'latest_activities': activities,
        'latest_books': BukuSerializer(latest_books, many=True).data,
        'latest_schools': schools_data
    }
    
    return Response(stats)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_users(request):
    role = request.GET.get('role', '')
    
    # Dapatkan semua user dengan role yang diminta
    users = User.objects.filter(role=role)
    
    # Exclude user yang sudah memiliki guru/siswa
    if role == 'guru':
        used_users = guru.objects.values_list('user_id', flat=True)
        users = users.exclude(id__in=used_users)
    elif role == 'siswa':
        used_users = siswa.objects.values_list('user_id', flat=True)
        users = users.exclude(id__in=used_users)
    
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user, context={'request': request})
        user_data = serializer.data

        # Tambahkan data spesifik berdasarkan peran
        if user.role == 'guru':
            try:
                guru_instance = guru.objects.get(user=user)
                kelas_list = [{
                    'id': kelas.id,
                    'nama_kelas': kelas.nama_kelas
                } for kelas in guru_instance.kelas.all()]
                
                user_data.update({
                    'nama': guru_instance.nama_guru,
                    'nama_mata_pelajaran': guru_instance.nama_mata_pelajaran.id,
                    'nama_mata_pelajaran_detail': {
                        'id': guru_instance.nama_mata_pelajaran.id,
                        'nama_mata_pelajaran': guru_instance.nama_mata_pelajaran.nama_mata_pelajaran
                    },
                    'kelas': [k['id'] for k in kelas_list],  # List of kelas IDs
                    'kelas_detail': kelas_list,  # List of kelas objects with id and nama_kelas
                    'jenjang': guru_instance.jenjang.id,
                    'jenjang_detail': {
                        'id': guru_instance.jenjang.id,
                        'nama_jenjang': guru_instance.jenjang.nama_jenjang
                    },
                    'sekolah': guru_instance.sekolah.id,
                    'sekolah_detail': {
                        'id': guru_instance.sekolah.id,
                        'nama_sekolah': guru_instance.sekolah.nama_sekolah,
                        'logo': guru_instance.sekolah.logo_sekolah.url if guru_instance.sekolah.logo_sekolah else None
                    },
                    'crud_buku': guru_instance.crud_buku,
                    'crud_materi': guru_instance.crud_materi
                })
            except guru.DoesNotExist:
                pass
        elif user.role == 'siswa':
            try:
                siswa_instance = siswa.objects.get(user=user)
                user_data.update({
                    'nama': siswa_instance.nama_siswa,
                    'kelas': {
                        'id': siswa_instance.kelas.id,
                        'nama_kelas': siswa_instance.kelas.nama_kelas
                    },
                    'jenjang': {
                        'id': siswa_instance.jenjang.id,
                        'nama_jenjang': siswa_instance.jenjang.nama_jenjang
                    },
                    'sekolah_detail': {
                        'id': siswa_instance.sekolah.id,
                        'nama_sekolah': siswa_instance.sekolah.nama_sekolah,
                        'logo': siswa_instance.sekolah.logo_sekolah.url if siswa_instance.sekolah.logo_sekolah else None
                    } if siswa_instance.sekolah else None
                })
            except siswa.DoesNotExist:
                pass

        return Response(user_data)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data

        # Update user fields
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.address = data.get('address', user.address)
        user.tanggal_lahir = data.get('tanggal_lahir', user.tanggal_lahir)

        if 'password' in data and data['password']:
            user.set_password(data['password'])

        # Handle file upload
        if 'foto_profil' in request.FILES:
            user.foto_profil = request.FILES['foto_profil']

        user.save()

        # Update role-specific fields
        if user.role == 'guru':
            try:
                guru_instance = guru.objects.get(user=user)
                if 'nama_mata_pelajaran' in data:
                    guru_instance.nama_mata_pelajaran_id = data['nama_mata_pelajaran']
                if 'kelas' in data:
                    guru_instance.kelas_id = data['kelas']
                if 'jenjang' in data:
                    guru_instance.jenjang_id = data['jenjang']
                if 'sekolah' in data:
                    guru_instance.sekolah_id = data['sekolah']
                guru_instance.save()
            except guru.DoesNotExist:
                pass
        elif user.role == 'siswa':
            try:
                siswa_instance = siswa.objects.get(user=user)
                if 'kelas' in data:
                    siswa_instance.kelas_id = data['kelas']
                if 'jenjang' in data:
                    siswa_instance.jenjang_id = data['jenjang']
                if 'sekolah' in data:
                    siswa_instance.sekolah_id = data['sekolah']
                siswa_instance.save()
            except siswa.DoesNotExist:
                pass

        # Return updated data
        return self.get(request)

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        try:
            ids = request.data.get('ids', [])
            if not ids:
                return Response(
                    {'error': 'Tidak ada ID yang diberikan'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            User.objects.filter(id__in=ids).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_siswa_profile(request):
    try:
        user = request.user
        if user.role != 'siswa':
            return Response(
                {'error': 'Hanya siswa yang dapat mengakses endpoint ini'},
                status=status.HTTP_403_FORBIDDEN
            )

        siswa_data = siswa.objects.select_related(
            'user',
            'kelas',
            'jenjang',
            'sekolah'
        ).get(user=user)

        data = {
            'id': siswa_data.id,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'nama_siswa': siswa_data.nama_siswa,
            'kelas_detail': {
                'id': siswa_data.kelas.id,
                'nama_kelas': siswa_data.kelas.nama_kelas
            } if siswa_data.kelas else None,
            'jenjang_detail': {
                'id': siswa_data.jenjang.id,
                'nama_jenjang': siswa_data.jenjang.nama_jenjang
            } if siswa_data.jenjang else None,
            'sekolah_detail': {
                'id': siswa_data.sekolah.id,
                'nama_sekolah': siswa_data.sekolah.nama_sekolah
            } if siswa_data.sekolah else None
        }
        
        return Response(data)

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
def get_siswa_by_user(request, user_id):
    try:
        siswa_data = siswa.objects.select_related(
            'user',
            'kelas',
            'jenjang',
            'sekolah'
        ).get(user_id=user_id)

        data = {
            'id': siswa_data.id,
            'nama_siswa': siswa_data.nama_siswa,
            'kelas_detail': {
                'id': siswa_data.kelas.id,
                'nama_kelas': siswa_data.kelas.nama_kelas
            } if siswa_data.kelas else None,
            'jenjang_detail': {
                'id': siswa_data.jenjang.id,
                'nama_jenjang': siswa_data.jenjang.nama_jenjang
            } if siswa_data.jenjang else None,
            'sekolah_detail': {
                'id': siswa_data.sekolah.id,
                'nama_sekolah': siswa_data.sekolah.nama_sekolah
            } if siswa_data.sekolah else None
        }
        
        return Response(data)

    except siswa.DoesNotExist:
        return Response(
            {'error': 'Data siswa tidak ditemukan'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
