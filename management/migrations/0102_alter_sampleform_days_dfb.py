# Generated by Django 4.1 on 2023-07-11 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0101_alter_sampleform_dfb_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleform',
            name='days_dfb',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
