from django.db import models

# Create your models here.
class sekolah(models.Model):
    nama_sekolah = models.CharField(max_length=255)
    logo_sekolah =  models.ImageField(upload_to='logo_sekolah/', blank=True, null=True)
    
    class Meta:
      db_table = 'sekolah'
      verbose_name_plural = 'sekolah'
      
    def __str__(self):
      return self.nama_sekolah
      
class jenjang(models.Model):
    nama_jenjang = models.CharField(max_length=255)
    
    class Meta:
      db_table = 'janjang'
      verbose_name_plural = 'jenjang'
      
    def __str__(self):
      return self.nama_jenjang
      
class kelas(models.Model):
    jenjang = models.ForeignKey('atribut.jenjang', on_delete=models.CASCADE)
    nama_kelas = models.CharField(max_length=255)
    
    class Meta:
      db_table = 'kelas'
      verbose_name_plural = 'kelas'
      

    def __str__(self):
      return self.nama_kelas
      
class mata_pelajaran(models.Model):
    nama_mata_pelajaran = models.CharField(max_length=255)
    
    class Meta:
      db_table = 'mata_pelajaran'
      verbose_name_plural = 'mata_pelajaran'
      
    def __str__(self):
      return self.nama_mata_pelajaran
      
      


