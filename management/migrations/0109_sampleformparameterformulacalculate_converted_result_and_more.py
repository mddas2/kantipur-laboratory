# Generated by Django 4.1 on 2023-07-12 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0108_merge_20230711_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='converted_result',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='decimal_place',
            field=models.CharField(max_length=200, null=True),
        ),
    ]