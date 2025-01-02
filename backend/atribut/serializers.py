from rest_framework import serializers
from .models import sekolah, jenjang, kelas, mata_pelajaran

class SekolahSerializer(serializers.ModelSerializer):
    class Meta:
        model = sekolah
        fields = '__all__'

class JenjangSerializer(serializers.ModelSerializer):
    class Meta:
        model = jenjang
        fields = '__all__'

class KelasSerializer(serializers.ModelSerializer):
    jenjang_detail = JenjangSerializer(source='jenjang', read_only=True)
    
    class Meta:
        model = kelas
        fields = ['id', 'nama_kelas', 'jenjang', 'jenjang_detail']

class MataPelajaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = mata_pelajaran
        fields = '__all__' 
