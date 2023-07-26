# Generated by Django 4.1 on 2023-07-16 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0117_microparameter_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='microparameter',
            name='is_original',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='rawdatasheetdetail',
            name='micro_table',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='raw_data', to='management.microparameter'),
        ),
    ]