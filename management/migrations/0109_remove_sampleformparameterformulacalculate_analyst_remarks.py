# Generated by Django 4.1 on 2023-07-12 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0108_sampleformparameterformulacalculate_converted_result_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sampleformparameterformulacalculate',
            name='analyst_remarks',
        ),
    ]
