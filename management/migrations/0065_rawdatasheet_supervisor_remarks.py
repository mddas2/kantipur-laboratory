# Generated by Django 4.1 on 2023-06-26 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0064_alter_sampleform_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawdatasheet',
            name='supervisor_remarks',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]