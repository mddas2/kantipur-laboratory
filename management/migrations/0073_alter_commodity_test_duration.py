# Generated by Django 4.1 on 2023-06-27 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0072_remove_testresult_notation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodity',
            name='test_duration',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
