# Generated by Django 4.1 on 2023-05-18 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0002_sampleformparameterformulacalculate_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleform',
            name='supervisor_user',
            field=models.ManyToManyField(default=None, related_name='sample_has_parameters', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='auto_calculate_result',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='commodity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.commodity'),
        ),
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='input_fields_value',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='parameter',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.testresult'),
        ),
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='sample_form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result', to='management.sampleform'),
        ),
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='updated_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]