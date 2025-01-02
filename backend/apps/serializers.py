from rest_framework import serializers
from .models import buku, perangkat_kurikulum, materi
from atribut.serializers import KelasSerializer, JenjangSerializer, MataPelajaranSerializer, SekolahSerializer
from users.serializers import GuruSerializer, UserSerializer
import os

class BukuSerializer(serializers.ModelSerializer):
    kelas_detail = KelasSerializer(source='kelas', read_only=True)
    jenjang_detail = JenjangSerializer(source='jenjang', read_only=True)
    mata_pelajaran_detail = MataPelajaranSerializer(source='mata_pelajaran', read_only=True)
    sekolah_detail = SekolahSerializer(source='sekolah', read_only=True)
    
    class Meta:
        model = buku
        fields = '__all__'
        
    def validate_file_buku(self, value):
        if value:
            # Validasi ekstensi file
            ext = os.path.splitext(value.name)[1].lower()
            valid_extensions = ['.pdf', '.doc', '.docx']
            
            if ext not in valid_extensions:
                raise serializers.ValidationError(
                    'Format file tidak valid. Gunakan PDF, DOC, atau DOCX'
                )
                
            # Validasi ukuran file (max 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError(
                    'Ukuran file terlalu besar. Maksimal 10MB'
                )
                
        return value

    def validate(self, data):
        # Log data yang diterima untuk debugging
        print("Data yang diterima:", data)
        
        if not self.instance:  # Jika creating new buku
            if not data.get('file_buku'):
                raise serializers.ValidationError({
                    'file_buku': 'File buku harus diunggah untuk buku baru'
                })
                
        required_fields = {
            'nama_buku': 'Nama buku',
            'penerbit': 'Penerbit',
            'kelas': 'Kelas',
            'jenjang': 'Jenjang',
            'mata_pelajaran': 'Mata pelajaran'
        }
        
        errors = {}
        for field, label in required_fields.items():
            if field not in data:
                errors[field] = f'{label} harus diisi'
                
        if errors:
            raise serializers.ValidationError(errors)
                
        return data 

class BulkDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        error_messages={
            'empty': 'Minimal satu ID harus dipilih',
            'invalid': 'Format ID tidak valid'
        }
    ) 

class PerangkatKurikulumSerializer(serializers.ModelSerializer):
    kelas_detail = KelasSerializer(source='kelas', read_only=True)
    jenjang_detail = JenjangSerializer(source='jenjang', read_only=True)
    mata_pelajaran_detail = MataPelajaranSerializer(source='mata_pelajaran', read_only=True)
    sekolah_detail = SekolahSerializer(source='sekolah', read_only=True)
    guru_detail = UserSerializer(source='guru', read_only=True)
    
    class Meta:
        model = perangkat_kurikulum
        fields = '__all__'
        read_only_fields = ('guru',)
        
    def validate_file_perangkat_kurikulum(self, value):
        # Jika dalam mode update dan tidak ada file baru
        if self.instance and not value:
            return self.instance.file_perangkat_kurikulum
        
        if value:
            # Validasi ekstensi file
            ext = os.path.splitext(value.name)[1].lower()
            valid_extensions = ['.pdf', '.doc', '.docx']
            
            if ext not in valid_extensions:
                raise serializers.ValidationError(
                    'Format file tidak valid. Gunakan PDF, DOC, atau DOCX'
                )
                
            # Validasi ukuran file (max 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError(
                    'Ukuran file terlalu besar. Maksimal 10MB'
                )
        
        return value
        
    def validate(self, data):
        if self.instance:  # Mode update
            # Jika tidak ada file baru yang dikirim, kembalikan data apa adanya
            if 'file_perangkat_kurikulum' not in data:
                return data
            
        # Mode create atau update dengan file baru
        required_fields = {
            'nama_perangkat_kurikulum': 'Nama perangkat kurikulum',
            'kelas': 'Kelas',
            'jenjang': 'Jenjang', 
            'mata_pelajaran': 'Mata pelajaran',
            'sekolah': 'Sekolah'
        }
        
        errors = {}
        for field, label in required_fields.items():
            if field not in data:
                errors[field] = f'{label} harus diisi'
                
        # Hanya validasi file jika mode create
        if not self.instance and 'file_perangkat_kurikulum' not in data:
            errors['file_perangkat_kurikulum'] = 'File perangkat kurikulum harus diunggah'
            
        if errors:
            raise serializers.ValidationError(errors)
            
        return data

class MateriSerializer(serializers.ModelSerializer):
    guru_detail = serializers.SerializerMethodField()
    sekolah_detail = serializers.SerializerMethodField()
    kelas_detail = serializers.SerializerMethodField()
    jenjang_detail = serializers.SerializerMethodField()
    mata_pelajaran_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = materi
        fields = '__all__'
        read_only_fields = ('guru',)
    
    def get_guru_detail(self, obj):
        if obj.guru:
            return {
                'id': obj.guru.id,
                'username': obj.guru.username,
                'email': obj.guru.email
            }
        return None
        
    def get_sekolah_detail(self, obj):
        if obj.sekolah:
            return {
                'id': obj.sekolah.id,
                'nama_sekolah': obj.sekolah.nama_sekolah
            }
        return None
        
    def get_kelas_detail(self, obj):
        if obj.kelas:
            return {
                'id': obj.kelas.id,
                'nama_kelas': obj.kelas.nama_kelas
            }
        return None
        
    def get_jenjang_detail(self, obj):
        if obj.jenjang:
            return {
                'id': obj.jenjang.id,
                'nama_jenjang': obj.jenjang.nama_jenjang
            }
        return None
        
    def get_mata_pelajaran_detail(self, obj):
        if obj.mata_pelajaran:
            return {
                'id': obj.mata_pelajaran.id,
                'nama_mata_pelajaran': obj.mata_pelajaran.nama_mata_pelajaran
            }
        return None

    def validate_file_materi(self, value):
        if value:
            # Validasi ekstensi file
            ext = os.path.splitext(value.name)[1].lower()
            valid_extensions = ['.pdf', '.doc', '.docx']
            
            if ext not in valid_extensions:
                raise serializers.ValidationError(
                    'Format file tidak valid. Gunakan PDF, DOC, atau DOCX'
                )
                
            # Validasi ukuran file (max 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError(
                    'Ukuran file terlalu besar. Maksimal 10MB'
                )
        return value

    def validate_status(self, value):
        valid_choices = ['aktif', 'tidak_aktif']
        if value not in valid_choices:
            raise serializers.ValidationError(f"Status harus salah satu dari: {', '.join(valid_choices)}")
        return value

    def validate(self, data):
        if 'status' not in data:
            data['status'] = 'aktif'
        return data
