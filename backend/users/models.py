from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('guru', 'Guru'),
        ('siswa', 'Siswa'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    foto_profil = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'users' 
        

class guru(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guru')
    nama_guru = models.CharField(max_length=100)
    nama_mata_pelajaran = models.ForeignKey('atribut.mata_pelajaran', on_delete=models.CASCADE)
    kelas = models.ManyToManyField('atribut.kelas')
    jenjang = models.ForeignKey('atribut.jenjang', on_delete=models.SET_NULL, null=True)
    sekolah = models.ForeignKey('atribut.sekolah', on_delete=models.SET_NULL, null=True)
    crud_buku = models.BooleanField(default=False) # Baru
    crud_materi = models.BooleanField(default=False) # Baru
    
    class Meta:
        db_table = 'guru'
        verbose_name_plural = 'guru'
        
class siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='siswa')
    nama_siswa = models.CharField(max_length=100)
    kelas = models.ForeignKey('atribut.kelas', on_delete=models.SET_NULL, null=True)
    jenjang = models.ForeignKey('atribut.jenjang', on_delete=models.SET_NULL, null=True)
    sekolah = models.ForeignKey('atribut.sekolah', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'siswa'
        verbose_name_plural = 'siswa'
        
