# Generated by Django 4.1 on 2023-07-16 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0118_microparameter_is_original_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleform',
            name='admin_remarks',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='sampleform',
            name='verifier_remarks',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
