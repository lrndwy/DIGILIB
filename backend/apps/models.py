from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Create your models here.
class buku(models.Model):
    nama_buku = models.CharField(max_length=255)
    file_buku = models.FileField(upload_to='buku/', null=True, blank=True)
    penerbit = models.CharField(max_length=255)
    kelas = models.ForeignKey('atribut.kelas', on_delete=models.CASCADE)
    jenjang = models.ForeignKey('atribut.jenjang', on_delete=models.CASCADE)
    mata_pelajaran = models.ForeignKey('atribut.mata_pelajaran', on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('aktif', 'Aktif'),
        ('tidak_aktif', 'Tidak Aktif'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aktif')
    sekolah = models.ForeignKey('atribut.sekolah', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = 'buku'
        verbose_name_plural = 'buku'
        
    def __str__(self):
      return self.nama_buku

class perangkat_kurikulum(models.Model):
    nama_perangkat_kurikulum = models.CharField(max_length=255)
    file_perangkat_kurikulum = models.FileField(upload_to='perangkat_kurikulum', null=True, blank=True)
    kelas = models.ForeignKey('atribut.kelas', on_delete=models.CASCADE)
    jenjang = models.ForeignKey('atribut.jenjang', on_delete=models.CASCADE)
    mata_pelajaran = models.ForeignKey('atribut.mata_pelajaran', on_delete=models.CASCADE)
    guru = models.ForeignKey('users.user', on_delete=models.CASCADE)
    sekolah = models.ForeignKey('atribut.sekolah', on_delete=models.CASCADE)
    
    
    class Meta:
        db_table = 'perangkat_kurikulum'
        verbose_name_plural = 'perangkat_kurikulum'
        
    def __str__(self):
      return self.nama_perangkat_kurikulum
        
class materi(models.Model):
    nama_materi = models.CharField(max_length=255)
    file_materi = models.FileField(upload_to='materi', null=True, blank=True)
    guru = models.ForeignKey('users.user', on_delete=models.CASCADE)
    sekolah = models.ForeignKey('atribut.sekolah', on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('aktif', 'Aktif'),
        ('tidak_aktif', 'Tidak Aktif'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aktif')
    kelas = models.ForeignKey('atribut.kelas', on_delete=models.CASCADE)
    jenjang = models.ForeignKey('atribut.jenjang', on_delete=models.CASCADE)
    mata_pelajaran = models.ForeignKey('atribut.mata_pelajaran', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'materi'
        verbose_name_plural = 'materi'
        
    def __str__(self):
      return self.nama_materi
        
# Signal untuk menghapus file ketika model dihapus
@receiver(pre_delete, sender=buku)
def delete_buku_file(sender, instance, **kwargs):
    if instance.file_buku:
        instance.file_buku.delete(False)

@receiver(pre_delete, sender=perangkat_kurikulum)
def delete_perangkat_file(sender, instance, **kwargs):
    if instance.file_perangkat_kurikulum:
        instance.file_perangkat_kurikulum.delete(False)

@receiver(pre_delete, sender=materi)
def delete_materi_file(sender, instance, **kwargs):
    if instance.file_materi:
        instance.file_materi.delete(False)
