# Generated by Django 4.1 on 2023-06-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0075_alter_sampleform_requested_export'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleform',
            name='requested_export',
            field=models.CharField(max_length=155, null=True),
        ),
    ]
