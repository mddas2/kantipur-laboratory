# Generated by Django 4.1 on 2023-05-30 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0022_sampleformparameterformulacalculate_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleformhasparameter',
            name='status',
            field=models.CharField(blank=True, choices=[('processing', 'processing'), ('completed', 'completed')], max_length=155, null=True),
        ),
        migrations.AlterField(
            model_name='sampleformparameterformulacalculate',
            name='parameter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.testresult'),
        ),
    ]