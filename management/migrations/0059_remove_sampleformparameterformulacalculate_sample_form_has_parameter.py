# Generated by Django 4.1 on 2023-06-23 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0058_alter_sampleformparameterformulacalculate_sample_form_has_parameter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sampleformparameterformulacalculate',
            name='sample_form_has_parameter',
        ),
    ]
