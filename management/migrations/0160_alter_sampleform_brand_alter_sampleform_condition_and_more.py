# Generated by Django 4.1 on 2023-08-17 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0159_alter_sampleform_dfb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleform',
            name='brand',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sampleform',
            name='condition',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sampleform',
            name='purpose',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
