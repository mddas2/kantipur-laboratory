# Generated by Django 4.1 on 2023-06-30 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0076_alter_sampleform_requested_export'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuperVisorSampleForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_supervisor_sent', models.BooleanField(default=False)),
                ('status', models.CharField(blank=True, choices=[('pending', 'pending'), ('processing', 'processing'), ('completed', 'completed'), ('recheck', 'recheck'), ('rejected', 'rejected'), ('not_verified', 'not_verified'), ('verified', 'verified')], default='pending', max_length=155, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('remarks', models.CharField(max_length=1000, null=True)),
                ('parameter', models.ManyToManyField(related_name='supervisor_has_parameter', to='management.testresult')),
                ('sample_form', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supervisor_sample_form', to='management.sampleform')),
                ('supervisor_user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
