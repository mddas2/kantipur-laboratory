# Generated by Django 4.1 on 2023-06-30 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0078_rename_parameter_supervisorsampleform_parameters'),
    ]

    operations = [
        migrations.AddField(
            model_name='supervisorsampleform',
            name='test_type',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
