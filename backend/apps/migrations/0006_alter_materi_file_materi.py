# Generated by Django 5.1.4 on 2025-01-02 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_alter_materi_guru'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materi',
            name='file_materi',
            field=models.FileField(blank=True, null=True, upload_to='materi'),
        ),
    ]
