# Generated by Django 4.1 on 2023-07-10 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0091_rename_analyst_encode_id_sampleform_refrence_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
    ]
