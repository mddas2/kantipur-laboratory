# Generated by Django 4.1 on 2023-06-23 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0050_alter_sampleform_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleformhasparameter',
            name='remarks',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='sampleformverifier',
            name='remarks',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]