from rest_framework import serializers
from .models import User, guru, siswa
from django.conf import settings
from atribut.serializers import MataPelajaranSerializer, KelasSerializer, JenjangSerializer, SekolahSerializer
from atribut.models import mata_pelajaran, kelas, jenjang, sekolah

class UserSerializer(serializers.ModelSerializer):
    foto_profil_url = serializers.SerializerMethodField()
    nama = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'is_active', 'foto_profil', 'foto_profil_url', 'address', 'tanggal_lahir', 'phone', 'nama')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'foto_profil': {'required': False},
            'nama': {'read_only': True}
        }

    def get_foto_profil_url(self, obj):
        try:
            if obj.foto_profil and hasattr(obj.foto_profil, 'url'):
                request = self.context.get('request')
                if request is not None:
                    return request.build_absolute_uri(obj.foto_profil.url)
                return obj.foto_profil.url
        except Exception as e:
            print(f"Error getting foto_profil_url: {str(e)}")
        return None

    def get_nama(self, obj):
        if obj.role == 'guru':
            try:
                return obj.guru.nama_guru
            except guru.DoesNotExist:
                return None
        elif obj.role == 'siswa':
            try:
                return obj.siswa.nama_siswa
            except siswa.DoesNotExist:
                return None
        return None

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
        
    def update(self, instance, validated_data):
        if 'password' in validated_data and validated_data['password']:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class GuruSerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()
    nama_mata_pelajaran_detail = serializers.SerializerMethodField()
    kelas_detail = serializers.SerializerMethodField()
    jenjang_detail = serializers.SerializerMethodField()
    sekolah_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = guru
        fields = '__all__'
        
    def get_user_detail(self, obj):
        return {
            'username': obj.user.username,
            'id': obj.user.id
        }
        
    def get_nama_mata_pelajaran_detail(self, obj):
        if obj.nama_mata_pelajaran:
            return {
                'id': obj.nama_mata_pelajaran.id,
                'nama_mata_pelajaran': obj.nama_mata_pelajaran.nama_mata_pelajaran
            }
        return None
        
    def get_kelas_detail(self, obj):
        return [{
            'id': kelas.id,
            'nama_kelas': kelas.nama_kelas
        } for kelas in obj.kelas.all()]
        
    def get_jenjang_detail(self, obj):
        if obj.jenjang:
            return {
                'id': obj.jenjang.id,
                'nama_jenjang': obj.jenjang.nama_jenjang
            }
        return None
        
    def get_sekolah_detail(self, obj):
        if obj.sekolah:
            return {
                'id': obj.sekolah.id,
                'nama_sekolah': obj.sekolah.nama_sekolah
            }
        return None

    def validate(self, data):
        # Validasi user unik
        user = data.get('user')
        instance = self.instance
        
        if guru.objects.filter(user=user).exclude(id=getattr(instance, 'id', None)).exists():
            raise serializers.ValidationError({'user': 'User ini sudah terdaftar sebagai guru'})
        
        return data

class SiswaSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    kelas_detail = KelasSerializer(source='kelas', read_only=True)
    jenjang_detail = JenjangSerializer(source='jenjang', read_only=True)
    sekolah_detail = SekolahSerializer(source='sekolah', read_only=True)
    
    class Meta:
        model = siswa
        fields = (
            'id',
            'user',
            'user_detail',
            'nama_siswa',
            'kelas',
            'kelas_detail',
            'jenjang',
            'jenjang_detail',
            'sekolah',
            'sekolah_detail'
        )

    def validate(self, data):
        # Validasi user unik
        user = data.get('user')
        instance = self.instance
        
        if siswa.objects.filter(user=user).exclude(id=getattr(instance, 'id', None)).exists():
            raise serializers.ValidationError({'user': 'User ini sudah terdaftar sebagai siswa'})
        
        return data
